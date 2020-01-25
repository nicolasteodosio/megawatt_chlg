from django.shortcuts import resolve_url
from django.test import TestCase
from model_mommy import mommy

from app.models import Plant


class TestPlantList(TestCase):

    def test_list_plants(self):
        mommy.make(Plant, _quantity=15)
        response = self.client.get(resolve_url('plant_list'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content.decode('utf-8'))

    def test_list_plants_when_empty(self):
        response = self.client.get(resolve_url('plant_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[]')
