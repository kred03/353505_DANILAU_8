from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re
from .models import (
    AnimalClass, AnimalFamily, HabitatCountry, FeedType, Enclosure, Employee, Animal, Feeding,
    Promotion, Coupon
)

# Отменяем стандартную регистрацию User
admin.site.unregister(User)

# Регистрируем свою версию админки для User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

def validate_phone(value):
    """
    +375 (29) 123-45-67
    +375291234567
    375291234567
    8 029 123-45-67
    """
    # Удаляем все не цифры для проверки длины
    cleaned_number = re.sub(r'\D', '', value)
    
    # Проверяем длину (9 цифр для номера + 3 цифры код страны)
    if len(cleaned_number) not in [12, 13]:  # 12 для формата 375... и 13 для +375...
        raise ValidationError('Номер телефона должен содержать 12 или 13 цифр')
    
    # Проверяем формат с помощью регулярного выражения
    patterns = [
        r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',  # +375 (29) 123-45-67
        r'^\+375\d{9}$',                          # +375291234567
        r'^375\d{9}$',                            # 375291234567
        r'^8 0\d{2} \d{3}-\d{2}-\d{2}$'          # 8 029 123-45-67
    ]
    
    if not any(re.match(pattern, value) for pattern in patterns):
        raise ValidationError(
            'Неверный формат номера. Допустимые форматы:\n'
            '+375 (29) 123-45-67\n'
            '+375291234567\n'
            '375291234567\n'
            '8 029 123-45-67'
        )

@admin.register(AnimalClass)
class AnimalClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(AnimalFamily)
class AnimalFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_class')
    search_fields = ('name', 'description')
    list_filter = ('animal_class',)

@admin.register(HabitatCountry)
class HabitatCountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FeedType)
class FeedTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'area', 'has_water')
    search_fields = ('name', 'number', 'description')
    list_filter = ('has_water',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'position', 'phone')
    filter_horizontal = ('assigned_animals', 'assigned_enclosures')
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'ФИО'

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'animal_class', 'family', 'enclosure', 'is_active')
    search_fields = ('name', 'species', 'description')
    list_filter = ('animal_class', 'family', 'enclosure', 'is_active')
    filter_horizontal = ('habitat_countries', 'feed_types')

@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):
    list_display = ('animal', 'feed_type', 'amount', 'feeding_time', 'date', 'employee')
    search_fields = ('animal__name', 'feed_type__name', 'employee__user__first_name', 'employee__user__last_name')
    list_filter = ('date', 'feed_type')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'description')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'fixed_discount', 'valid_from', 'valid_until', 'is_active', 'one_time_use')
    list_filter = ('is_active', 'one_time_use')
    search_fields = ('code', 'description') 