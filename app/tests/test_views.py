import json

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


class TestPlantDetail(TestCase):

    def test_get_plant(self):
        mommy.make(Plant, id=555)
        response = self.client.get(resolve_url('plant_detail', 555))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def test_get_plant_dont_exist(self):
        mommy.make(Plant, id=555)
        response = self.client.get(resolve_url('plant_detail', 78))

        self.assertEqual(response.status_code, 404)

    def test_plant_detail_method_not_allowed(self):
        mommy.make(Plant, id=555)
        response = self.client.post(resolve_url('plant_detail', 555))

        self.assertEqual(response.status_code, 405)

    def test_update_plant(self):
        mommy.make(Plant, id=44, name="plant1")
        payload = {
            'name': 'plant2'
        }
        self.assertEqual(Plant.objects.get(id=44).name, 'plant1')
        response = self.client.put(resolve_url('plant_detail', 44), json.dumps(payload),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Plant.objects.get(id=44).name, 'plant2')

    def test_update_plant_if_exists(self):
        mommy.make(Plant, id=44, name="plant1")
        payload = {
            'nome': 'plant2'
        }
        response = self.client.put(resolve_url('plant_detail', 99), json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_delete_plant(self):
        plant = mommy.make(Plant)
        response = self.client.delete(resolve_url('plant_detail', plant.id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(list(Plant.objects.filter(id=plant.id)), [])

    def test_delete_plant_if_exists(self):
        response = self.client.delete(resolve_url('plant_detail', 456))

        self.assertEqual(response.status_code, 404)
