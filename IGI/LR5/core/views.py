from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login
from django import forms
from .models import (
    AnimalClass, AnimalFamily, HabitatCountry, FeedType, Enclosure, Employee, Animal, Feeding,
    Promotion, Coupon, News, FAQ, Job, Review, Client
)
import requests
from django.db import models
import logging
from django.db.models import Count, Sum, Avg, ExpressionWrapper, FloatField, F
from django.db.models.functions import Cast
import json
from .forms import ClientRegistrationForm, NewsForm, JobForm, PromotionForm, CouponForm, AnimalForm, EnclosureForm, AnimalClassForm, AnimalFamilyForm, FeedTypeForm, EmployeeForm, FAQForm
import random
import calendar
from datetime import datetime, timedelta
from django.http import HttpResponseNotAllowed

logger = logging.getLogger(__name__)

# Главная страница
class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animals_count'] = Animal.objects.count()
        context['enclosures_count'] = Enclosure.objects.count()
        context['employees_count'] = Employee.objects.count()
        context['news'] = News.objects.filter(is_published=True)[:3]
        # --- Альтернативные API ---
        # Факт о животном (кошка)
        animal_fact = None
        try:
            resp = requests.get('https://catfact.ninja/fact', timeout=5)
            if resp.ok:
                animal_fact = resp.json().get('fact')
        except Exception:
            pass
        if not animal_fact:
            try:
                resp = requests.get('https://meow.senither.com/v1/facts', timeout=5)
                if resp.ok:
                    facts = resp.json().get('data', [])
                    if facts:
                        animal_fact = random.choice(facts)
            except Exception:
                pass
        context['animal_fact'] = animal_fact or 'Не удалось получить факт.'
        # Картинка животного (собака или кошка)
        animal_image = None
        try:
            resp = requests.get('https://dog.ceo/api/breeds/image/random', timeout=5)
            if resp.ok:
                animal_image = resp.json().get('message')
        except Exception:
            pass
        if not animal_image:
            try:
                resp = requests.get('https://cataas.com/cat?json=true', timeout=5)
                if resp.ok:
                    data = resp.json()
                    if 'url' in data:
                        animal_image = 'https://cataas.com' + data['url']
            except Exception:
                pass
        context['animal_image'] = animal_image or '/static/images/animal_placeholder.png'
        # Погода (open-meteo.com, Минск)
        weather = None
        try:
            resp = requests.get('https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.5667&current_weather=true', timeout=5)
            if resp.ok:
                data = resp.json()
                w = data.get('current_weather', {})
                if w:
                    temp = w.get('temperature')
                    wind = w.get('windspeed')
                    weather = f"Температура: {temp}°C, Ветер: {wind} км/ч"
        except Exception:
            pass
        context['weather'] = weather or 'Не удалось получить погоду.'
        # Текстовый календарь на чистом Python (без import calendar)
        now = timezone.now()
        year = now.year
        month = now.month
        # Определяем первый день месяца и количество дней
        first_day = datetime(year, month, 1)
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        num_days = (next_month - first_day).days
        # День недели первого дня (0 - понедельник)
        first_weekday = (first_day.weekday())  # 0 - понедельник
        week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        cal_lines = []
        cal_lines.append(f'{now.strftime("%B %Y").capitalize():^20}')
        cal_lines.append(' '.join(week_days))
        week = ['  '] * 7
        day = 1
        # Заполняем первую неделю
        for i in range(first_weekday, 7):
            week[i] = f'{day:2d}'
            day += 1
        cal_lines.append(' '.join(week))
        # Остальные недели
        while day <= num_days:
            week = []
            for i in range(7):
                if day <= num_days:
                    week.append(f'{day:2d}')
                    day += 1
                else:
                    week.append('  ')
            cal_lines.append(' '.join(week))
        calendar_text = '\n'.join(cal_lines)
        context['calendar_text'] = calendar_text
        return context

def about_view(request):
    return render(request, 'core/about.html')

@login_required
def profile_view(request):
    employee = Employee.objects.filter(user=request.user).first()
    client = Client.objects.filter(user=request.user).first()
    return render(request, 'core/profile.html', {'employee': employee, 'client': client})

# --- Животные ---
class AnimalListView(ListView):
    """
    Список животных с поддержкой поиска и сортировки.
    Поиск по имени, виду, описанию, классу, семейству.
    Сортировка по имени, дате поступления, классу, семейству.
    """
    model = Animal
    template_name = 'core/animal_list.html'
    context_object_name = 'animals'
    paginate_by = 20

    def get_queryset(self):
        queryset = Animal.objects.all()
        q = self.request.GET.get('q', '').strip()
        sort = self.request.GET.get('sort', '')
        self.search_warning = None
        valid_sorts = {'', 'name', 'name_desc', 'arrival', 'arrival_desc', 'class', 'family'}
        if sort not in valid_sorts:
            self.sort_warning = 'Некорректный параметр сортировки.'
        else:
            self.sort_warning = None
        if q:
            if len(q) < 2:
                self.search_warning = 'Введите минимум 2 символа для поиска.'
            else:
                logger.info(f'Поиск животных: {q}')
                queryset = queryset.filter(
                    models.Q(name__icontains=q) |
                    models.Q(species__icontains=q) |
                    models.Q(description__icontains=q) |
                    models.Q(animal_class__name__icontains=q) |
                    models.Q(family__name__icontains=q)
                )
        if sort and sort in valid_sorts:
            logger.info(f'Сортировка животных: {sort}')
        if sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'arrival':
            queryset = queryset.order_by('arrival_date')
        elif sort == 'arrival_desc':
            queryset = queryset.order_by('-arrival_date')
        elif sort == 'class':
            queryset = queryset.order_by('animal_class__name')
        elif sort == 'family':
            queryset = queryset.order_by('family__name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'search_warning') and self.search_warning:
            context['search_warning'] = self.search_warning
        if hasattr(self, 'sort_warning') and self.sort_warning:
            context['sort_warning'] = self.sort_warning
        return context

class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'core/animal_detail.html'
    context_object_name = 'animal'

# --- Помещения ---
class EnclosureListView(ListView):
    model = Enclosure
    template_name = 'core/enclosure_list.html'
    context_object_name = 'enclosures'
    paginate_by = 20

class EnclosureDetailView(DetailView):
    model = Enclosure
    template_name = 'core/enclosure_detail.html'
    context_object_name = 'enclosure'

class EnclosureCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Enclosure
    form_class = EnclosureForm
    template_name = 'core/enclosure_form.html'
    success_url = reverse_lazy('enclosure-list')
    def test_func(self):
        return self.request.user.is_superuser

class EnclosureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Enclosure
    form_class = EnclosureForm
    template_name = 'core/enclosure_form.html'
    success_url = reverse_lazy('enclosure-list')
    def test_func(self):
        return self.request.user.is_superuser

class EnclosureDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Enclosure
    template_name = 'core/enclosure_confirm_delete.html'
    success_url = reverse_lazy('enclosure-list')
    def test_func(self):
        return self.request.user.is_superuser

# --- Кормления ---
class FeedingListView(ListView):
    model = Feeding
    template_name = 'core/feeding_list.html'
    context_object_name = 'feedings'
    paginate_by = 20

# --- Сотрудники ---
class EmployeeListView(ListView):
    model = Employee
    template_name = 'core/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'core/employee_form.html'
    success_url = reverse_lazy('employee-list')
    def test_func(self):
        return self.request.user.is_superuser

class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'core/employee_form.html'
    success_url = reverse_lazy('employee-list')
    def test_func(self):
        return self.request.user.is_superuser

class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'core/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')
    def test_func(self):
        return self.request.user.is_superuser

# --- Классы и семейства ---
class AnimalClassListView(ListView):
    model = AnimalClass
    template_name = 'core/animalclass_list.html'
    context_object_name = 'classes'
    paginate_by = 20

class AnimalFamilyListView(ListView):
    model = AnimalFamily
    template_name = 'core/animalfamily_list.html'
    context_object_name = 'families'
    paginate_by = 20

# --- Корма ---
class FeedTypeListView(ListView):
    model = FeedType
    template_name = 'core/feedtype_list.html'
    context_object_name = 'feedtypes'
    paginate_by = 20

# --- Промокоды и купоны ---
class PromotionCouponListView(ListView):
    template_name = 'core/promotion_coupon_list.html'
    context_object_name = 'promos'

    def get_queryset(self):
        return list(Promotion.objects.filter(is_active=True)) + list(Coupon.objects.filter(is_active=True))

# --- Новости, FAQ, Вакансии, Отзывы (оставляем как есть) ---
class NewsListView(ListView):
    model = News
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

class NewsDetailView(DetailView):
    model = News
    template_name = 'core/news_detail.html'
    context_object_name = 'news'

class FAQListView(ListView):
    model = FAQ
    template_name = 'core/faq_list.html'
    context_object_name = 'faqs'

class JobListView(ListView):
    model = Job
    template_name = 'core/job_list.html'
    context_object_name = 'jobs'

class ReviewListView(ListView):
    model = Review
    template_name = 'core/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 20

class ReviewCreateView(CreateView):
    model = Review
    fields = ['text', 'rating']
    template_name = 'core/review_form.html'
    success_url = reverse_lazy('review-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['text', 'rating']
    template_name = 'core/review_form.html'
    success_url = reverse_lazy('review-list')
    def test_func(self):
        return self.request.user.is_superuser

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'core/review_confirm_delete.html'
    success_url = reverse_lazy('review-list')
    def test_func(self):
        return self.request.user.is_superuser

class InterestingView(TemplateView):
    template_name = 'core/interesting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # API факт о животном
        try:
            animal_resp = requests.get('https://some-random-api.ml/animal/cat', timeout=5)
            if animal_resp.ok:
                animal_data = animal_resp.json()
                context['animal_fact'] = animal_data.get('fact')
                context['animal_image'] = animal_data.get('image')
            else:
                context['animal_fact'] = 'Не удалось получить факт.'
                context['animal_image'] = None
        except Exception:
            context['animal_fact'] = 'Ошибка при обращении к API.'
            context['animal_image'] = None
        # API погоды
        try:
            weather_resp = requests.get('https://wttr.in/?format=3', timeout=5)
            if weather_resp.ok:
                context['weather'] = weather_resp.text
            else:
                context['weather'] = 'Не удалось получить погоду.'
        except Exception:
            context['weather'] = 'Ошибка при обращении к погодному API.'
        return context

def statistics(request):
    # Основные показатели
    total_animals = Animal.objects.count()
    total_enclosures = Enclosure.objects.count()
    total_employees = Employee.objects.count()
    feedings_per_day = Feeding.objects.filter(
        date=timezone.now().date()
    ).count()

    # Статистика по классам животных
    animals_by_class = Animal.objects.values('animal_class__name').annotate(
        count=Count('id')
    ).order_by('-count')
    animal_classes = [item['animal_class__name'] for item in animals_by_class]
    animals_by_class = [item['count'] for item in animals_by_class]

    # Статистика заполненности помещений
    enclosures = Enclosure.objects.all()
    enclosure_names = [enc.name for enc in enclosures]
    enclosure_occupancy = [enc.animal_set.count() for enc in enclosures]

    # Статистика кормлений
    feeding_stats = Feeding.objects.values('feed_type__name').annotate(
        feeding_count=Count('id'),
        total_amount=Sum('amount'),
        avg_amount=Avg('amount')
    ).order_by('-feeding_count')
    total_feedings = Feeding.objects.count()

    # Статистика сотрудников
    employee_stats = Employee.objects.annotate(
        feeding_count=Count('feeding'),
        animal_count=Count('assigned_animals'),
        enclosure_count=Count('assigned_enclosures'),
        efficiency=ExpressionWrapper(
            (F('feeding_count') * 100.0) / Cast(total_feedings, FloatField()),
            output_field=FloatField()
        )
    ).order_by('-efficiency')

    context = {
        'total_animals': total_animals,
        'total_enclosures': total_enclosures,
        'total_employees': total_employees,
        'feedings_per_day': feedings_per_day,
        'animal_classes': json.dumps(animal_classes),
        'animals_by_class': json.dumps(animals_by_class),
        'enclosure_names': json.dumps(enclosure_names),
        'enclosure_occupancy': json.dumps(enclosure_occupancy),
        'feeding_stats': feeding_stats,
        'total_feedings': total_feedings,
        'employee_stats': employee_stats,
    }
    return render(request, 'core/statistics.html', context)

def register_view(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = ClientRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'core/news_form.html'
    success_url = reverse_lazy('news-list')
    def test_func(self):
        return self.request.user.is_superuser

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'core/news_form.html'
    success_url = reverse_lazy('news-list')
    def test_func(self):
        return self.request.user.is_superuser

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'core/news_confirm_delete.html'
    success_url = reverse_lazy('news-list')
    def test_func(self):
        return self.request.user.is_superuser

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'core/job_form.html'
    success_url = reverse_lazy('job-list')
    def test_func(self):
        return self.request.user.is_superuser

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'core/job_form.html'
    success_url = reverse_lazy('job-list')
    def test_func(self):
        return self.request.user.is_superuser

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'core/job_confirm_delete.html'
    success_url = reverse_lazy('job-list')
    def test_func(self):
        return self.request.user.is_superuser

class PromotionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'core/promotion_form.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class PromotionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'core/promotion_form.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class PromotionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Promotion
    template_name = 'core/promotion_confirm_delete.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class CouponCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'core/coupon_form.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class CouponUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'core/coupon_form.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class CouponDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Coupon
    template_name = 'core/coupon_confirm_delete.html'
    success_url = reverse_lazy('promotion-coupon-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'core/animal_form.html'
    success_url = reverse_lazy('animal-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'core/animal_form.html'
    success_url = reverse_lazy('animal-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Animal
    template_name = 'core/animal_confirm_delete.html'
    success_url = reverse_lazy('animal-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalClassCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AnimalClass
    form_class = AnimalClassForm
    template_name = 'core/animalclass_form.html'
    success_url = reverse_lazy('animalclass-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalClassUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AnimalClass
    form_class = AnimalClassForm
    template_name = 'core/animalclass_form.html'
    success_url = reverse_lazy('animalclass-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalClassDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnimalClass
    template_name = 'core/animalclass_confirm_delete.html'
    success_url = reverse_lazy('animalclass-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalFamilyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AnimalFamily
    form_class = AnimalFamilyForm
    template_name = 'core/animalfamily_form.html'
    success_url = reverse_lazy('animalfamily-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalFamilyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AnimalFamily
    form_class = AnimalFamilyForm
    template_name = 'core/animalfamily_form.html'
    success_url = reverse_lazy('animalfamily-list')
    def test_func(self):
        return self.request.user.is_superuser

class AnimalFamilyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnimalFamily
    template_name = 'core/animalfamily_confirm_delete.html'
    success_url = reverse_lazy('animalfamily-list')
    def test_func(self):
        return self.request.user.is_superuser

class FeedTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FeedType
    form_class = FeedTypeForm
    template_name = 'core/feedtype_form.html'
    success_url = reverse_lazy('feedtype-list')
    def test_func(self):
        return self.request.user.is_superuser

class FeedTypeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeedType
    form_class = FeedTypeForm
    template_name = 'core/feedtype_form.html'
    success_url = reverse_lazy('feedtype-list')
    def test_func(self):
        return self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class FeedTypeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FeedType
    template_name = 'core/feedtype_confirm_delete.html'
    success_url = reverse_lazy('feedtype-list')
    def test_func(self):
        return self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class FAQCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'core/faq_form.html'
    success_url = reverse_lazy('faq-list')
    def test_func(self):
        return self.request.user.is_superuser

class FAQUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'core/faq_form.html'
    success_url = reverse_lazy('faq-list')
    def test_func(self):
        return self.request.user.is_superuser

class FAQDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FAQ
    template_name = 'core/faq_confirm_delete.html'
    success_url = reverse_lazy('faq-list')
    def test_func(self):
        return self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST']) 