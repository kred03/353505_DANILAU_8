from django.test import TestCase
from django.urls import reverse
from .models import Animal, AnimalClass, AnimalFamily

class AnimalListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cls1 = AnimalClass.objects.create(name='Млекопитающие')
        cls.fam1 = AnimalFamily.objects.create(name='Кошачьи', animal_class=cls.cls1)
        cls.animal1 = Animal.objects.create(name='Барсик', animal_class=cls.cls1, family=cls.fam1, species='Кот', arrival_date='2020-01-01')
        cls.animal2 = Animal.objects.create(name='Шарик', animal_class=cls.cls1, family=cls.fam1, species='Собака', arrival_date='2021-01-01')

    def test_search_by_name(self):
        response = self.client.get(reverse('animal-list'), {'q': 'Барсик'})
        self.assertContains(response, 'Барсик')
        self.assertNotContains(response, 'Шарик')

    def test_search_too_short(self):
        response = self.client.get(reverse('animal-list'), {'q': 'Б'})
        self.assertContains(response, 'Введите минимум 2 символа для поиска.')

    def test_sort_by_name_desc(self):
        response = self.client.get(reverse('animal-list'), {'sort': 'name_desc'})
        animals = list(response.context['animals'])
        self.assertEqual(animals[0].name, 'Шарик')
        self.assertEqual(animals[1].name, 'Барсик')

    def test_invalid_sort(self):
        response = self.client.get(reverse('animal-list'), {'sort': 'invalid'})
        self.assertContains(response, 'Некорректный параметр сортировки.') 