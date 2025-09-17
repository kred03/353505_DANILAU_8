from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('statistics/', views.statistics, name='statistics'),

    # Животные
    path('animals/', views.AnimalListView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(), name='animal-detail'),
    path('animals/create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('animals/<int:pk>/edit/', views.AnimalUpdateView.as_view(), name='animal-update'),
    path('animals/<int:pk>/delete/', views.AnimalDeleteView.as_view(), name='animal-delete'),

    # Помещения
    path('enclosures/', views.EnclosureListView.as_view(), name='enclosure-list'),
    path('enclosures/<int:pk>/', views.EnclosureDetailView.as_view(), name='enclosure-detail'),
    path('enclosures/create/', views.EnclosureCreateView.as_view(), name='enclosure-create'),
    path('enclosures/<int:pk>/edit/', views.EnclosureUpdateView.as_view(), name='enclosure-update'),
    path('enclosures/<int:pk>/delete/', views.EnclosureDeleteView.as_view(), name='enclosure-delete'),

    # Кормления
    path('feedings/', views.FeedingListView.as_view(), name='feeding-list'),

    # Сотрудники
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),

    # Классы и семейства
    path('animal-classes/', views.AnimalClassListView.as_view(), name='animalclass-list'),
    path('animal-classes/create/', views.AnimalClassCreateView.as_view(), name='animalclass-create'),
    path('animal-classes/<int:pk>/edit/', views.AnimalClassUpdateView.as_view(), name='animalclass-update'),
    path('animal-classes/<int:pk>/delete/', views.AnimalClassDeleteView.as_view(), name='animalclass-delete'),
    path('animal-families/', views.AnimalFamilyListView.as_view(), name='animalfamily-list'),
    path('animal-families/create/', views.AnimalFamilyCreateView.as_view(), name='animalfamily-create'),
    path('animal-families/<int:pk>/edit/', views.AnimalFamilyUpdateView.as_view(), name='animalfamily-update'),
    path('animal-families/<int:pk>/delete/', views.AnimalFamilyDeleteView.as_view(), name='animalfamily-delete'),

    # Корма
    path('feed-types/', views.FeedTypeListView.as_view(), name='feedtype-list'),
    path('feed-types/create/', views.FeedTypeCreateView.as_view(), name='feedtype-create'),
    path('feed-types/<int:pk>/edit/', views.FeedTypeUpdateView.as_view(), name='feedtype-update'),
    path('feed-types/<int:pk>/delete/', views.FeedTypeDeleteView.as_view(), name='feedtype-delete'),

    # Промокоды и купоны
    path('promotions-and-coupons/', views.PromotionCouponListView.as_view(), name='promotion-coupon-list'),
    path('promotions/create/', views.PromotionCreateView.as_view(), name='promotion-create'),
    path('promotions/<int:pk>/edit/', views.PromotionUpdateView.as_view(), name='promotion-update'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion-delete'),
    path('coupons/create/', views.CouponCreateView.as_view(), name='coupon-create'),
    path('coupons/<int:pk>/edit/', views.CouponUpdateView.as_view(), name='coupon-update'),
    path('coupons/<int:pk>/delete/', views.CouponDeleteView.as_view(), name='coupon-delete'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('register/', views.register_view, name='register'),  # если потребуется регистрация

    # Новости
    path('news/', views.NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('news/create/', views.NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),

    # FAQ
    path('faq/', views.FAQListView.as_view(), name='faq-list'),
    path('faq/create/', views.FAQCreateView.as_view(), name='faq-create'),
    path('faq/<int:pk>/edit/', views.FAQUpdateView.as_view(), name='faq-update'),
    path('faq/<int:pk>/delete/', views.FAQDeleteView.as_view(), name='faq-delete'),

    # Вакансии
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job-update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),

    # Отзывы
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/new/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),

    path('interesting/', views.InterestingView.as_view(), name='interesting'),

    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
] 