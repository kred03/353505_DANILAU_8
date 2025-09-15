from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Product, Partner, CompanyInfo, CompanyHistory, Contact, Dictionary,
    News, FAQ, Job, Review, Promotion, Coupon
)
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными для ЛР 1 HTML'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем заполнение базы данных...')
        
        # Создаем товары
        self.create_products()
        
        # Создаем партнеров
        self.create_partners()
        
        # Создаем информацию о компании
        self.create_company_info()
        
        # Создаем контакты
        self.create_contacts()
        
        # Создаем словарь терминов
        self.create_dictionary()
        
        # Создаем новости
        self.create_news()
        
        # Создаем FAQ
        self.create_faq()
        
        # Создаем вакансии
        self.create_jobs()
        
        # Создаем отзывы
        self.create_reviews()
        
        # Создаем промокоды и купоны
        self.create_promotions()
        
        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )

    def create_products(self):
        products_data = [
            {
                'name': 'Экскурсия по зоопарку',
                'description': 'Увлекательная экскурсия по территории зоопарка с опытным гидом. Вы узнаете много интересного о жизни животных и их повадках.',
                'price': Decimal('15.00'),
                'category': 'экскурсии'
            },
            {
                'name': 'Кормление животных',
                'description': 'Уникальная возможность покормить животных под присмотром специалистов. Включено в стоимость корм.',
                'price': Decimal('25.00'),
                'category': 'услуги'
            },
            {
                'name': 'Фотосессия с животными',
                'description': 'Профессиональная фотосессия с любимыми животными зоопарка. Фотографии на память включены.',
                'price': Decimal('50.00'),
                'category': 'услуги'
            },
            {
                'name': 'Сувенирный магнит',
                'description': 'Красивый магнит с изображением животных зоопарка. Отличный подарок на память.',
                'price': Decimal('5.00'),
                'category': 'сувениры'
            },
            {
                'name': 'Детский билет',
                'description': 'Билет для детей от 3 до 12 лет. Включает посещение всех экспозиций зоопарка.',
                'price': Decimal('8.00'),
                'category': 'билеты'
            },
            {
                'name': 'Взрослый билет',
                'description': 'Билет для взрослых посетителей. Включает посещение всех экспозиций зоопарка.',
                'price': Decimal('12.00'),
                'category': 'билеты'
            },
            {
                'name': 'Семейный билет',
                'description': 'Выгодный билет для семьи из 4 человек (2 взрослых + 2 ребенка).',
                'price': Decimal('35.00'),
                'category': 'билеты'
            },
            {
                'name': 'Годовой абонемент',
                'description': 'Неограниченное посещение зоопарка в течение года. Включает все мероприятия и скидки.',
                'price': Decimal('100.00'),
                'category': 'билеты'
            }
        ]
        
        for product_data in products_data:
            Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
        
        self.stdout.write('Создано товаров: {}'.format(len(products_data)))

    def create_partners(self):
        partners_data = [
            {
                'name': 'Беларусбанк',
                'description': 'Официальный банк-партнер зоопарка. Предоставляет льготные условия для посетителей.',
                'website_url': 'https://www.belarusbank.by'
            },
            {
                'name': 'МТС',
                'description': 'Телекоммуникационный партнер. Специальные предложения для абонентов МТС.',
                'website_url': 'https://www.mts.by'
            },
            {
                'name': 'БелАЗ',
                'description': 'Промышленный партнер. Поддержка образовательных программ зоопарка.',
                'website_url': 'https://www.belaz.by'
            },
            {
                'name': 'Минский зоопарк',
                'description': 'Коллеги из столичного зоопарка. Обмен опытом и совместные программы.',
                'website_url': 'https://www.minskzoo.by'
            },
            {
                'name': 'WWF Беларусь',
                'description': 'Всемирный фонд дикой природы. Совместные проекты по сохранению природы.',
                'website_url': 'https://www.wwf.by'
            },
            {
                'name': 'Белорусский государственный университет',
                'description': 'Образовательный партнер. Научные исследования и студенческие практики.',
                'website_url': 'https://www.bsu.by'
            }
        ]
        
        for partner_data in partners_data:
            Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
        
        self.stdout.write('Создано партнеров: {}'.format(len(partners_data)))

    def create_company_info(self):
        company_info, created = CompanyInfo.objects.get_or_create(
            title='Зоопарк "Дикая природа"',
            defaults={
                'description': '''Добро пожаловать в зоопарк "Дикая природа" - уникальное место, где вы можете познакомиться с удивительным миром животных со всего света. 

Наш зоопарк был основан в 1995 году с целью сохранения и изучения дикой природы, а также просвещения посетителей о важности защиты окружающей среды.

Мы гордимся тем, что предоставляем животным комфортные условия жизни, максимально приближенные к их естественной среде обитания. Наши специалисты работают круглосуточно, чтобы обеспечить лучший уход за нашими питомцами.

Зоопарк активно участвует в международных программах по сохранению исчезающих видов и проводит образовательные программы для детей и взрослых.''',
                'requisites': '''ООО "Зоопарк Дикая природа"
УНП: 123456789
Юридический адрес: г. Минск, ул. Зоологическая, 1
Банк: ОАО "Беларусбанк"
БИК: 153001369
р/с: BY86BLBB3014000000000000000001
Телефон: +375 17 123-45-67
Email: info@zoo.by''',
                'certificate_text': '''СЕРТИФИКАТ О ЧЛЕНСТВЕ В РТА
(РЕЕСТР ТУРИСТИЧЕСКИХ АГЕНТСТВ) 
АССОЦИАЦИИ ТУРПОМОЩЬ

г. Минск, 15 января 2024

Настоящим удостоверяется, что

Общество с ограниченной ответственностью «Зоопарк Дикая природа» (УНП 123456789)

внесено в Единый реестр туристических агентств Ассоциации "ТУРПОМОЩЬ" под номером 2024.

Директор Ассоциации "ТУРПОМОЩЬ"
Иванов И.И.

Контактная информация Ассоциации "ТУРПОМОЩЬ":
Адрес: 220000, г. Минск, ул. Советская, 15
Телефон: +375 17 234-56-78
E-mail: office@tourpom.by'''
            }
        )
        
        if created:
            # Создаем историю компании
            history_data = [
                {'year': 1995, 'title': 'Основание зоопарка', 'description': 'Зоопарк "Дикая природа" был основан группой энтузиастов-зоологов.'},
                {'year': 2000, 'title': 'Первая международная программа', 'description': 'Запуск программы по обмену животными с европейскими зоопарками.'},
                {'year': 2005, 'title': 'Открытие образовательного центра', 'description': 'Создание центра для проведения образовательных программ и экскурсий.'},
                {'year': 2010, 'title': 'Сертификация', 'description': 'Получение сертификата качества от международной ассоциации зоопарков.'},
                {'year': 2015, 'title': 'Модернизация', 'description': 'Крупная реконструкция и модернизация вольеров и инфраструктуры.'},
                {'year': 2020, 'title': 'Цифровизация', 'description': 'Внедрение современных технологий и создание виртуальных туров.'},
                {'year': 2024, 'title': 'Новые программы', 'description': 'Запуск интерактивных программ и расширение образовательных услуг.'}
            ]
            
            for history_item in history_data:
                CompanyHistory.objects.create(
                    company_info=company_info,
                    year=history_item['year'],
                    title=history_item['title'],
                    description=history_item['description']
                )
        
        self.stdout.write('Создана информация о компании')

    def create_contacts(self):
        contacts_data = [
            {
                'name': 'Анна Петровна Смирнова',
                'position': 'Директор зоопарка',
                'phone': '+375 17 123-45-67',
                'email': 'director@zoo.by',
                'description': 'Руководит работой зоопарка, отвечает за стратегическое планирование и развитие.'
            },
            {
                'name': 'Иван Михайлович Козлов',
                'position': 'Главный ветеринар',
                'phone': '+375 17 123-45-68',
                'email': 'vet@zoo.by',
                'description': 'Обеспечивает медицинское обслуживание всех животных зоопарка.'
            },
            {
                'name': 'Елена Владимировна Волкова',
                'position': 'Заведующая образовательным отделом',
                'phone': '+375 17 123-45-69',
                'email': 'education@zoo.by',
                'description': 'Организует экскурсии, лекции и образовательные программы.'
            },
            {
                'name': 'Сергей Александрович Медведев',
                'position': 'Главный зоолог',
                'phone': '+375 17 123-45-70',
                'email': 'zoologist@zoo.by',
                'description': 'Отвечает за научную работу и изучение поведения животных.'
            },
            {
                'name': 'Мария Сергеевна Лебедева',
                'position': 'Менеджер по туризму',
                'phone': '+375 17 123-45-71',
                'email': 'tourism@zoo.by',
                'description': 'Организует туристические программы и групповые посещения.'
            }
        ]
        
        for contact_data in contacts_data:
            Contact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
        
        self.stdout.write('Создано контактов: {}'.format(len(contacts_data)))

    def create_dictionary(self):
        dictionary_data = [
            {
                'term': 'Зоопарк',
                'definition': 'Учреждение для содержания и демонстрации диких животных в неволе с целью их изучения, разведения и просвещения населения.'
            },
            {
                'term': 'Вольер',
                'definition': 'Огороженное пространство для содержания животных, максимально приближенное к их естественной среде обитания.'
            },
            {
                'term': 'Экскурсия',
                'definition': 'Организованное посещение зоопарка с гидом, включающее рассказ о животных, их повадках и особенностях.'
            },
            {
                'term': 'Кормление',
                'definition': 'Процесс предоставления пищи животным, включающий специальные рационы и режимы питания.'
            },
            {
                'term': 'Ветеринар',
                'definition': 'Специалист по лечению и профилактике заболеваний животных.'
            },
            {
                'term': 'Зоолог',
                'definition': 'Ученый, изучающий поведение, физиологию и экологию животных.'
            },
            {
                'term': 'Акклиматизация',
                'definition': 'Процесс приспособления животных к новым условиям жизни в зоопарке.'
            },
            {
                'term': 'Энричмент',
                'definition': 'Обогащение среды обитания животных для повышения их активности и благополучия.'
            },
            {
                'term': 'Консервация',
                'definition': 'Сохранение исчезающих видов животных через программы разведения в неволе.'
            },
            {
                'term': 'Биоразнообразие',
                'definition': 'Разнообразие живых организмов в экосистеме, включая генетическое, видовое и экосистемное разнообразие.'
            }
        ]
        
        for term_data in dictionary_data:
            Dictionary.objects.get_or_create(
                term=term_data['term'],
                defaults=term_data
            )
        
        self.stdout.write('Создано терминов: {}'.format(len(dictionary_data)))

    def create_news(self):
        news_data = [
            {
                'title': 'Новое пополнение в семье львов',
                'description': 'В зоопарке родились два львенка - самец и самка.',
                'content': 'Сегодня утром в зоопарке произошло радостное событие - у пары африканских львов родились детеныши. Мама-львица и малыши чувствуют себя хорошо. Посетители смогут увидеть новое семейство через несколько недель, когда львята окрепнут.'
            },
            {
                'title': 'Открытие нового павильона "Тропики"',
                'description': 'В зоопарке открылся новый павильон с тропическими животными.',
                'content': 'Сегодня состоялось торжественное открытие нового павильона "Тропики", где поселились экзотические животные из тропических лесов. В павильоне созданы условия, максимально приближенные к естественной среде обитания.'
            },
            {
                'title': 'Образовательная программа для школьников',
                'description': 'Зоопарк запускает новую образовательную программу для учащихся.',
                'content': 'С нового учебного года зоопарк предлагает школам специальную образовательную программу, включающую тематические экскурсии, лекции и практические занятия. Программа разработана с учетом школьной программы по биологии.'
            }
        ]
        
        for news_item in news_data:
            News.objects.get_or_create(
                title=news_item['title'],
                defaults=news_item
            )
        
        self.stdout.write('Создано новостей: {}'.format(len(news_data)))

    def create_faq(self):
        faq_data = [
            {
                'question': 'Какие часы работы зоопарка?',
                'answer': 'Зоопарк работает ежедневно с 9:00 до 18:00. В выходные и праздничные дни - с 9:00 до 19:00.'
            },
            {
                'question': 'Можно ли кормить животных?',
                'answer': 'Кормить животных можно только специальным кормом, который продается в зоопарке, и только в специально отведенных местах под присмотром сотрудников.'
            },
            {
                'question': 'Есть ли скидки для детей?',
                'answer': 'Да, для детей от 3 до 12 лет действует льготная цена билета. Дети до 3 лет проходят бесплатно.'
            },
            {
                'question': 'Можно ли прийти с собакой?',
                'answer': 'К сожалению, вход с домашними животными запрещен по соображениям безопасности.'
            },
            {
                'question': 'Есть ли парковка?',
                'answer': 'Да, на территории зоопарка есть бесплатная парковка для посетителей.'
            }
        ]
        
        for faq_item in faq_data:
            FAQ.objects.get_or_create(
                question=faq_item['question'],
                defaults=faq_item
            )
        
        self.stdout.write('Создано FAQ: {}'.format(len(faq_data)))

    def create_jobs(self):
        jobs_data = [
            {
                'title': 'Ветеринар',
                'description': 'Ищем опытного ветеринара для работы с экзотическими животными.',
                'requirements': 'Высшее ветеринарное образование, опыт работы с дикими животными не менее 3 лет.',
                'salary_from': Decimal('1500.00'),
                'salary_to': Decimal('2500.00')
            },
            {
                'title': 'Экскурсовод',
                'description': 'Требуется экскурсовод для проведения экскурсий по зоопарку.',
                'requirements': 'Высшее биологическое образование, коммуникативные навыки, знание иностранных языков приветствуется.',
                'salary_from': Decimal('800.00'),
                'salary_to': Decimal('1200.00')
            },
            {
                'title': 'Смотритель за животными',
                'description': 'Работа по уходу за животными и поддержанию чистоты в вольерах.',
                'requirements': 'Среднее образование, любовь к животным, физическая выносливость.',
                'salary_from': Decimal('600.00'),
                'salary_to': Decimal('900.00')
            }
        ]
        
        for job_data in jobs_data:
            Job.objects.get_or_create(
                title=job_data['title'],
                defaults=job_data
            )
        
        self.stdout.write('Создано вакансий: {}'.format(len(jobs_data)))

    def create_reviews(self):
        # Создаем тестового пользователя для отзывов
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )
        
        reviews_data = [
            {
                'user': user,
                'text': 'Отличный зоопарк! Животные ухоженные, территория чистая. Детям очень понравилось. Обязательно приедем еще!',
                'rating': 5
            },
            {
                'user': user,
                'text': 'Хорошее место для семейного отдыха. Много интересных животных, есть где погулять. Единственный минус - дорогие билеты.',
                'rating': 4
            },
            {
                'user': user,
                'text': 'Прекрасный зоопарк! Особенно понравились экскурсии с гидом. Очень познавательно и интересно.',
                'rating': 5
            }
        ]
        
        for review_data in reviews_data:
            Review.objects.get_or_create(
                user=review_data['user'],
                text=review_data['text'],
                defaults=review_data
            )
        
        self.stdout.write('Создано отзывов: {}'.format(len(reviews_data)))

    def create_promotions(self):
        # Создаем промокоды
        promotions_data = [
            {
                'code': 'WELCOME10',
                'description': 'Скидка 10% для новых посетителей',
                'discount_percent': 10,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=30)
            },
            {
                'code': 'WEEKEND20',
                'description': 'Скидка 20% на выходные',
                'discount_percent': 20,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=60)
            }
        ]
        
        for promo_data in promotions_data:
            Promotion.objects.get_or_create(
                code=promo_data['code'],
                defaults=promo_data
            )
        
        # Создаем купоны
        coupons_data = [
            {
                'code': 'FREETICKET',
                'description': 'Бесплатный детский билет',
                'fixed_discount': Decimal('8.00'),
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=30),
                'one_time_use': True
            },
            {
                'code': 'FAMILY5',
                'description': 'Скидка 5 рублей на семейный билет',
                'fixed_discount': Decimal('5.00'),
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=45),
                'one_time_use': False
            }
        ]
        
        for coupon_data in coupons_data:
            Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
        
        self.stdout.write('Создано промокодов и купонов: {}'.format(len(promotions_data) + len(coupons_data)))
