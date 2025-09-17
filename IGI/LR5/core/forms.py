from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
import uuid
from .models import Client, Organization, News, Animal, Enclosure, Feeding, Employee, FeedType, AnimalClass, AnimalFamily, Review, Job, FAQ, Promotion, Coupon
from .validators import validate_phone

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(
        max_length=20, 
        required=True,
        help_text='Формат: +375 (29) 123-45-67 или +375291234567'
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Вам должно быть не менее 18 лет'
    )
    organization_name = forms.CharField(max_length=100, required=False, help_text='Название организации (если есть)')
    organization_address = forms.CharField(max_length=200, required=False, help_text='Адрес организации (если есть)')
    organization_phone = forms.CharField(max_length=20, required=False, help_text='Телефон организации (если есть)')
    organization_email = forms.EmailField(required=False, help_text='Email организации (если есть)')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'phone', 'organization_name', 'organization_address', 'organization_phone', 'organization_email', 'password1', 'password2')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = relativedelta(today, birth_date).years
        if age < 18:
            raise ValidationError('Вам должно быть не менее 18 лет для регистрации.')
        return birth_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_phone(phone)
        return phone

    def clean_organization_phone(self):
        org_phone = self.cleaned_data.get('organization_phone')
        if org_phone:  # Проверяем только если телефон указан
            validate_phone(org_phone)
        return org_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Create or get organization if details provided
            organization = None
            if self.cleaned_data.get('organization_name'):
                organization = Organization.objects.create(
                    name=self.cleaned_data['organization_name'],
                    address=self.cleaned_data['organization_address'],
                    phone=self.cleaned_data['organization_phone'],
                    email=self.cleaned_data['organization_email']
                )
            
            # Create client profile
            Client.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date'],
                organization=organization
            )
        
        return user

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'animal_class', 'family', 'species', 'photo', 'birth_date', 'arrival_date', 'enclosure', 'habitat_countries', 'feed_types', 'description', 'is_active']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'habitat_countries': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'feed_types': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EnclosureForm(forms.ModelForm):
    class Meta:
        model = Enclosure
        fields = ['number', 'name', 'area', 'has_water', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'phone', 'position', 'photo', 'assigned_animals', 'assigned_enclosures']
        widgets = {
            'assigned_animals': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'assigned_enclosures': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class FeedTypeForm(forms.ModelForm):
    class Meta:
        model = FeedType
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AnimalClassForm(forms.ModelForm):
    class Meta:
        model = AnimalClass
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AnimalFamilyForm(forms.ModelForm):
    class Meta:
        model = AnimalFamily
        fields = ['name', 'animal_class', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'is_published']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'rows': 3}),
        }

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['code', 'description', 'discount_percent', 'valid_from', 'valid_until', 'is_active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'description', 'fixed_discount', 'valid_from', 'valid_until', 'is_active', 'one_time_use']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 