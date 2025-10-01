from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# --- Zoo Models ---

class AnimalClass(models.Model):
    """Класс животных (например, млекопитающие, птицы)"""
    name = models.CharField('Класс', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Класс животных'
        verbose_name_plural = 'Классы животных'

    def __str__(self):
        return self.name

class AnimalFamily(models.Model):
    """Семейство животных (например, кошачьи, псовые)"""
    name = models.CharField('Семейство', max_length=100)
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.CASCADE, verbose_name='Класс')
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Семейство животных'
        verbose_name_plural = 'Семейства животных'

    def __str__(self):
        return self.name

class HabitatCountry(models.Model):
    """Страна обитания"""
    name = models.CharField('Страна', max_length=100)

    class Meta:
        verbose_name = 'Страна обитания'
        verbose_name_plural = 'Страны обитания'

    def __str__(self):
        return self.name

class FeedType(models.Model):
    """Вид корма"""
    name = models.CharField('Вид корма', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Вид корма'
        verbose_name_plural = 'Виды корма'

    def __str__(self):
        return self.name

class Enclosure(models.Model):
    """Помещение/вольер"""
    number = models.CharField('Номер', max_length=20)
    name = models.CharField('Название', max_length=100)
    area = models.DecimalField('Площадь (кв.м)', max_digits=8, decimal_places=2)
    has_water = models.BooleanField('Есть водоем', default=False)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def __str__(self):
        return f"{self.name} (№{self.number})"

class Employee(models.Model):
    """Сотрудник зоопарка"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20)
    position = models.CharField('Должность', max_length=100)
    assigned_animals = models.ManyToManyField('Animal', blank=True, related_name='caretakers', verbose_name='Закрепленные животные')
    assigned_enclosures = models.ManyToManyField(Enclosure, blank=True, related_name='employees', verbose_name='Закрепленные помещения')
    photo = models.ImageField('Фото', upload_to='employees/', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.position})"

class Animal(models.Model):
    """Животное"""
    name = models.CharField('Кличка', max_length=100)
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.PROTECT, verbose_name='Класс')
    family = models.ForeignKey(AnimalFamily, on_delete=models.PROTECT, verbose_name='Семейство')
    species = models.CharField('Вид', max_length=100)
    photo = models.ImageField('Фото', upload_to='animals/', blank=True, null=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    arrival_date = models.DateField('Дата поступления в зоопарк')
    enclosure = models.ForeignKey(Enclosure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Помещение')
    habitat_countries = models.ManyToManyField(HabitatCountry, verbose_name='Страны обитания')
    feed_types = models.ManyToManyField(FeedType, verbose_name='Виды корма')
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('В зоопарке', default=True)

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return f"{self.name} ({self.species})"

class Feeding(models.Model):
    """Кормление животных"""
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name='Животное')
    feed_type = models.ForeignKey(FeedType, on_delete=models.PROTECT, verbose_name='Вид корма')
    amount = models.DecimalField('Количество (кг)', max_digits=6, decimal_places=2)
    feeding_time = models.TimeField('Время кормления')
    date = models.DateField('Дата кормления', default=timezone.now)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Кормление'
        verbose_name_plural = 'Кормления'
        ordering = ['-date', 'feeding_time']

    def __str__(self):
        return f"{self.animal} - {self.feed_type} ({self.amount} кг)"

# --- Promotions and Coupons (Zoo context) ---

class Promotion(models.Model):
    """Промокоды (скидки на билеты или услуги зоопарка)"""
    code = models.CharField('Код', max_length=20, unique=True)
    description = models.TextField('Описание')
    discount_percent = models.PositiveIntegerField('Скидка (%)', validators=[MinValueValidator(1)])
    valid_from = models.DateTimeField('Действует с')
    valid_until = models.DateTimeField('Действует до')
    is_active = models.BooleanField('Активен', default=True)
    # Можно добавить связь с услугами зоопарка, если появятся

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

class Coupon(models.Model):
    """Купоны (на доп. услуги, кормление животных и т.д.)"""
    code = models.CharField('Код', max_length=20, unique=True)
    description = models.TextField('Описание')
    fixed_discount = models.DecimalField('Фиксированная скидка', max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField('Действует с')
    valid_until = models.DateTimeField('Действует до')
    is_active = models.BooleanField('Активен', default=True)
    one_time_use = models.BooleanField('Одноразовый', default=True)
    # Можно добавить связь с услугами зоопарка, если появятся

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code

# --- News, FAQ, Job, Review (restored) ---

class News(models.Model):
    """Новости"""
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Краткое описание', default='')
    content = models.TextField('Содержание', default='')
    image = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class FAQ(models.Model):
    """Часто задаваемые вопросы"""
    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_at']

    def __str__(self):
        return self.question

class Job(models.Model):
    """Вакансии"""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    requirements = models.TextField('Требования')
    salary_from = models.DecimalField('Зарплата от', max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField('Зарплата до', max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.user.get_full_name() or self.user.username}'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20)
    birth_date = models.DateField('Дата рождения')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Организация')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Organization(models.Model):
    name = models.CharField('Название организации', max_length=100)
    address = models.CharField('Адрес', max_length=200, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name 