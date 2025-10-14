from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import AnimalClass, AnimalFamily, HabitatCountry, FeedType, Enclosure, Employee, Animal, Feeding, Promotion, Coupon, News, FAQ, Job, Review
import random
from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Наполняет зоопарк тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю наполнение зоопарка тестовыми данными...')

        # Создаем классы животных
        classes = [
            {'name': 'Млекопитающие', 'description': 'Класс позвоночных животных, питающихся молоком матери.'},
            {'name': 'Птицы', 'description': 'Класс теплокровных яйцекладущих позвоночных животных.'},
            {'name': 'Пресмыкающиеся', 'description': 'Класс позвоночных животных, включающий черепах, крокодилов, ящериц и змей.'}
        ]
        animal_classes = []
        for cls in classes:
            animal_class, created = AnimalClass.objects.get_or_create(name=cls['name'], defaults=cls)
            animal_classes.append(animal_class)
            self.stdout.write(f'Создан класс: {animal_class.name}')

        # Создаем семейства животных
        families = [
            {'name': 'Кошачьи', 'animal_class': animal_classes[0], 'description': 'Семейство млекопитающих отряда хищных.'},
            {'name': 'Собачьи', 'animal_class': animal_classes[0], 'description': 'Семейство млекопитающих отряда хищных.'},
            {'name': 'Попугаевые', 'animal_class': animal_classes[1], 'description': 'Семейство птиц отряда попугаеобразных.'},
            {'name': 'Змеи', 'animal_class': animal_classes[2], 'description': 'Семейство пресмыкающихся отряда чешуйчатых.'}
        ]
        animal_families = []
        for family in families:
            animal_family, created = AnimalFamily.objects.get_or_create(name=family['name'], defaults=family)
            animal_families.append(animal_family)
            self.stdout.write(f'Создано семейство: {animal_family.name}')

        # Создаем страны обитания
        countries = ['Африка', 'Азия', 'Европа', 'Северная Америка', 'Южная Америка']
        habitat_countries = []
        for country in countries:
            habitat_country, created = HabitatCountry.objects.get_or_create(name=country)
            habitat_countries.append(habitat_country)
            self.stdout.write(f'Создана страна обитания: {habitat_country.name}')

        # Создаем виды корма
        feed_types = [
            {'name': 'Мясо', 'description': 'Мясной корм для хищников.'},
            {'name': 'Рыба', 'description': 'Рыбный корм для хищников и всеядных.'},
            {'name': 'Фрукты', 'description': 'Фруктовый корм для травоядных и всеядных.'},
            {'name': 'Овощи', 'description': 'Овощной корм для травоядных и всеядных.'}
        ]
        feed_types_objects = []
        for feed in feed_types:
            feed_type, created = FeedType.objects.get_or_create(name=feed['name'], defaults=feed)
            feed_types_objects.append(feed_type)
            self.stdout.write(f'Создан вид корма: {feed_type.name}')

        # Создаем помещения
        enclosures = [
            {'name': 'Вольер для хищников', 'capacity': 5, 'description': 'Вольер для крупных хищников.'},
            {'name': 'Вольер для птиц', 'capacity': 10, 'description': 'Вольер для птиц.'},
            {'name': 'Террариум', 'capacity': 3, 'description': 'Террариум для пресмыкающихся.'}
        ]
        enclosure_objects = []
        for enc in enclosures:
            enclosure, created = Enclosure.objects.get_or_create(
                name=enc['name'],
                defaults={
                    'number': f"{enclosures.index(enc)+1}",
                    'area': [100.0, 50.0, 30.0][enclosures.index(enc)],
                    'has_water': enclosures.index(enc) == 0,  # только первый с водоемом
                    'description': enc['description']
                }
            )
            enclosure_objects.append(enclosure)
            self.stdout.write(f'Создано помещение: {enclosure.name}')

        # Создаем сотрудников
        employees = [
            {'username': 'employee1', 'password': 'password', 'first_name': 'Иван', 'last_name': 'Иванов'},
            {'username': 'employee2', 'password': 'password', 'first_name': 'Петр', 'last_name': 'Петров'},
            {'username': 'employee3', 'password': 'password', 'first_name': 'Сергей', 'last_name': 'Сидоров'},
            {'username': 'employee4', 'password': 'password', 'first_name': 'Анна', 'last_name': 'Кузнецова'},
            {'username': 'employee5', 'password': 'password', 'first_name': 'Мария', 'last_name': 'Васильева'},
            {'username': 'employee6', 'password': 'password', 'first_name': 'Алексей', 'last_name': 'Смирнов'},
            {'username': 'employee7', 'password': 'password', 'first_name': 'Ольга', 'last_name': 'Попова'},
            {'username': 'employee8', 'password': 'password', 'first_name': 'Дмитрий', 'last_name': 'Морозов'},
            {'username': 'employee9', 'password': 'password', 'first_name': 'Екатерина', 'last_name': 'Соколова'},
            {'username': 'employee10', 'password': 'password', 'first_name': 'Владимир', 'last_name': 'Новиков'},
        ]
        employee_objects = []
        for emp in employees:
            user, _ = User.objects.get_or_create(username=emp['username'], defaults={
                'first_name': emp['first_name'],
                'last_name': emp['last_name']
            })
            if not user.has_usable_password():
                user.set_password(emp['password'])
                user.save()
            employee, _ = Employee.objects.get_or_create(user=user)
            employee_objects.append(employee)
            self.stdout.write(f'Создан сотрудник: {employee.user.get_full_name()}')

        # Создаем животных
        animals = [
            {'name': 'Лев', 'animal_class': animal_classes[0], 'family': animal_families[0], 'species': 'Panthera leo', 'birth_date': timezone.now().date() - timedelta(days=365*5), 'arrival_date': timezone.now().date() - timedelta(days=365*2), 'enclosure': enclosure_objects[0], 'description': 'Крупный хищник семейства кошачьих.'},
            {'name': 'Орел', 'animal_class': animal_classes[1], 'family': animal_families[2], 'species': 'Aquila chrysaetos', 'birth_date': timezone.now().date() - timedelta(days=365*3), 'arrival_date': timezone.now().date() - timedelta(days=365*1), 'enclosure': enclosure_objects[1], 'description': 'Крупная хищная птица.'},
            {'name': 'Змея', 'animal_class': animal_classes[2], 'family': animal_families[3], 'species': 'Python regius', 'birth_date': timezone.now().date() - timedelta(days=365*2), 'arrival_date': timezone.now().date() - timedelta(days=365*1), 'enclosure': enclosure_objects[2], 'description': 'Крупная змея семейства питонов.'},
            {'name': 'Тигр', 'animal_class': animal_classes[0], 'family': animal_families[0], 'species': 'Panthera tigris', 'birth_date': timezone.now().date() - timedelta(days=365*4), 'arrival_date': timezone.now().date() - timedelta(days=365*2), 'enclosure': enclosure_objects[0], 'description': 'Полосатый хищник.'},
            {'name': 'Волк', 'animal_class': animal_classes[0], 'family': animal_families[1], 'species': 'Canis lupus', 'birth_date': timezone.now().date() - timedelta(days=365*6), 'arrival_date': timezone.now().date() - timedelta(days=365*3), 'enclosure': enclosure_objects[0], 'description': 'Серый волк — хищник из семейства псовых.'},
            {'name': 'Попугай', 'animal_class': animal_classes[1], 'family': animal_families[2], 'species': 'Ara ararauna', 'birth_date': timezone.now().date() - timedelta(days=365*2), 'arrival_date': timezone.now().date() - timedelta(days=365*1), 'enclosure': enclosure_objects[1], 'description': 'Яркая тропическая птица.'},
            {'name': 'Кобра', 'animal_class': animal_classes[2], 'family': animal_families[3], 'species': 'Naja naja', 'birth_date': timezone.now().date() - timedelta(days=365*3), 'arrival_date': timezone.now().date() - timedelta(days=365*2), 'enclosure': enclosure_objects[2], 'description': 'Ядовитая змея.'},
            {'name': 'Пантера', 'animal_class': animal_classes[0], 'family': animal_families[0], 'species': 'Panthera pardus', 'birth_date': timezone.now().date() - timedelta(days=365*7), 'arrival_date': timezone.now().date() - timedelta(days=365*4), 'enclosure': enclosure_objects[0], 'description': 'Грациозный хищник.'},
            {'name': 'Собака', 'animal_class': animal_classes[0], 'family': animal_families[1], 'species': 'Canis familiaris', 'birth_date': timezone.now().date() - timedelta(days=365*1), 'arrival_date': timezone.now().date() - timedelta(days=365*1), 'enclosure': enclosure_objects[0], 'description': 'Домашний друг человека.'},
            {'name': 'Жако', 'animal_class': animal_classes[1], 'family': animal_families[2], 'species': 'Psittacus erithacus', 'birth_date': timezone.now().date() - timedelta(days=365*2), 'arrival_date': timezone.now().date() - timedelta(days=365*1), 'enclosure': enclosure_objects[1], 'description': 'Попугай жако — умная птица.'},
        ]
        animal_objects = []
        for animal in animals:
            animal_obj, created = Animal.objects.get_or_create(name=animal['name'], defaults=animal)
            animal_obj.habitat_countries.add(*random.sample(habitat_countries, 2))
            animal_obj.feed_types.add(*random.sample(feed_types_objects, 2))
            animal_objects.append(animal_obj)
            self.stdout.write(f'Создано животное: {animal_obj.name}')

        # Создаем кормления
        for animal in animal_objects:
            for _ in range(3):
                feeding = Feeding.objects.create(
                    animal=animal,
                    feed_type=random.choice(feed_types_objects),
                    amount=random.uniform(1.0, 5.0),
                    date=timezone.now().date() - timedelta(days=random.randint(0, 30)),
                    feeding_time=timezone.now().time(),
                    employee=random.choice(employee_objects)
                )
                self.stdout.write(f'Создано кормление для {animal.name}')

        # Создаем новости
        news = [
            {'title': 'Новое поступление животных', 'description': 'В зоопарк поступили новые животные.', 'content': 'Недавно в наш зоопарк прибыли новые обитатели: тигр, попугай жако и кобра.', 'is_published': True, 'image': None},
            {'title': 'Ремонт вольеров', 'description': 'Проводится ремонт вольеров для улучшения условий содержания животных.', 'content': 'Вольеры для хищников и птиц обновляются для большего комфорта животных.', 'is_published': True, 'image': None},
            {'title': 'День открытых дверей', 'description': 'Приглашаем всех на день открытых дверей!', 'content': 'В этот день вход в зоопарк бесплатный для всех посетителей. Вас ждут экскурсии и мастер-классы.', 'is_published': True, 'image': 'news/otkrytye_dveri.jpg'},
            {'title': 'Появился новый жираф!', 'description': 'В нашем зоопарке появился жираф по имени Макс.', 'content': 'Макс быстро освоился и уже радует посетителей своим дружелюбием.', 'is_published': True, 'image': 'news/giraffe.jpg'},
            {'title': 'Экологическая акция', 'description': 'Собираем макулатуру и пластик для переработки.', 'content': 'Принесите вторсырьё и получите скидку на билет!', 'is_published': True, 'image': None},
            {'title': 'Ветеринарные лекции', 'description': 'Серия лекций для детей и взрослых о здоровье животных.', 'content': 'Наши ветеринары расскажут о правильном уходе за питомцами.', 'is_published': True, 'image': 'news/vet_lecture.jpg'},
            {'title': 'Праздник для детей', 'description': 'В зоопарке прошёл праздник для детей из детских домов.', 'content': 'Дети познакомились с животными и получили подарки.', 'is_published': True, 'image': None},
            {'title': 'Обновление меню кафе', 'description': 'В кафе зоопарка появились новые блюда.', 'content': 'Теперь вы можете попробовать свежие салаты и выпечку.', 'is_published': True, 'image': 'news/cafe.jpg'},
            {'title': 'Зимний режим работы', 'description': 'С 1 декабря зоопарк работает по зимнему расписанию.', 'content': 'Проверьте новые часы работы на нашем сайте.', 'is_published': True, 'image': None},
            {'title': 'Питомцы ищут дом', 'description': 'Некоторые животные ищут заботливых хозяев.', 'content': 'Если вы хотите взять питомца из зоопарка — обратитесь к сотрудникам.', 'is_published': True, 'image': 'news/adopt.jpg'},
        ]
        for n in news:
            news_obj, created = News.objects.get_or_create(title=n['title'], defaults={
                'description': n['description'],
                'content': n['content'],
                'is_published': n['is_published']
            })
            if n['image']:
                news_obj.image = n['image']
                news_obj.save()
            self.stdout.write(f'Создана новость: {news_obj.title}')

        # Создаем вакансии
        jobs = [
            {'title': 'Смотритель за животными', 'description': 'Требуется смотритель за животными.', 'is_active': True},
            {'title': 'Ветеринар', 'description': 'Требуется ветеринар для работы в зоопарке.', 'is_active': True}
        ]
        for job in jobs:
            job_obj, created = Job.objects.get_or_create(title=job['title'], defaults=job)
            self.stdout.write(f'Создана вакансия: {job_obj.title}')

        # Создаем промокоды
        now = timezone.now()
        promotions = [
            {
                'code': 'ZOO2023',
                'description': 'Скидка 10% на билеты в зоопарк',
                'discount_percent': 10,
                'valid_from': now,
                'valid_until': now + timedelta(days=365),
                'is_active': True
            },
            {
                'code': 'WELCOME',
                'description': 'Скидка 5% для новых посетителей',
                'discount_percent': 5,
                'valid_from': now,
                'valid_until': now + timedelta(days=365),
                'is_active': True
            }
        ]
        for promo in promotions:
            promo_obj, created = Promotion.objects.get_or_create(code=promo['code'], defaults=promo)
            self.stdout.write(f'Создан промокод: {promo_obj.code}')

        # Создаем купоны
        coupons = [
            {
                'code': 'SUMMER2023',
                'description': 'Купон на 15 рублей на услуги зоопарка',
                'fixed_discount': 15.0,
                'valid_from': now,
                'valid_until': now + timedelta(days=365),
                'is_active': True,
                'one_time_use': True
            },
            {
                'code': 'FAMILY',
                'description': 'Семейный купон на 20 рублей',
                'fixed_discount': 20.0,
                'valid_from': now,
                'valid_until': now + timedelta(days=365),
                'is_active': True,
                'one_time_use': False
            }
        ]
        for coupon in coupons:
            coupon_obj, created = Coupon.objects.get_or_create(code=coupon['code'], defaults=coupon)
            self.stdout.write(f'Создан купон: {coupon_obj.code}')

        # Создаем отзывы
        reviews = [
            {'username': 'user1', 'password': 'password', 'first_name': 'Алексей', 'last_name': 'Смирнов', 'content': 'Отличный зоопарк!', 'rating': 5},
            {'username': 'user2', 'password': 'password', 'first_name': 'Мария', 'last_name': 'Козлова', 'content': 'Очень понравилось!', 'rating': 4}
        ]
        for review in reviews:
            user, _ = User.objects.get_or_create(username=review['username'], defaults={
                'first_name': review['first_name'],
                'last_name': review['last_name']
            })
            if not user.has_usable_password():
                user.set_password(review['password'])
                user.save()
            review_obj, _ = Review.objects.get_or_create(user=user, defaults={'text': review['content'], 'rating': review['rating']})
            self.stdout.write(f'Создан отзыв от {review_obj.user.get_full_name()}')

        # Создаем FAQ
        faqs = [
            {'question': 'Какие животные есть в зоопарке?', 'answer': 'В зоопарке представлены млекопитающие, птицы и пресмыкающиеся.'},
            {'question': 'Как добраться до зоопарка?', 'answer': 'Зоопарк находится в центре города, добраться можно на общественном транспорте.'}
        ]
        for faq in faqs:
            faq_obj, created = FAQ.objects.get_or_create(question=faq['question'], defaults=faq)
            self.stdout.write(f'Создан FAQ: {faq_obj.question}')

        self.stdout.write(self.style.SUCCESS('Зоопарк успешно наполнен тестовыми данными!')) 