import json
from datetime import datetime
from unittest import mock

from django.shortcuts import resolve_url
from django.test import TestCase
from freezegun import freeze_time
from model_mommy import mommy

from app.models import Plant, Report


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

        self.assertEqual(response.status_code, 400)

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
        response = self.client.put(resolve_url('plant_detail', 99), json.dumps(payload),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_delete_plant(self):
        plant = mommy.make(Plant)
        response = self.client.delete(resolve_url('plant_detail', plant.id))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(list(Plant.objects.filter(id=plant.id)), [])

    def test_delete_plant_if_exists(self):
        response = self.client.delete(resolve_url('plant_detail', 456))

        self.assertEqual(response.status_code, 404)


class TestReportDetail(TestCase):

    def test_validate_plant_id_parameter_required(self):
        response = self.client.get(resolve_url('report_detail'), {'type': 'Energy', 'date': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'plant_id\' is a required property"]')

    def test_validate_plant_id_parameter_correct_pattern(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': 'TEST', 'type': 'Energy', 'date': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'TEST\' does not match \'^[0-9]*[1-9][0-9]*$\'"]')

    def test_validate_type_parameter_required(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'date': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'type\' is a required property"]')

    def test_validate_type_parameter_correct_type(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'date': '2020-01-01', 'type': 'test', })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'test\' is not one of [\'Energy\', \'Irradiation\']"]')

    def test_validate_date_parameter_required(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'type': 'Energy'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'date\' is a required property"]')

    def test_validate_date_parameter_correct_format(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'type': 'Energy', 'date': '2020/10/10'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         '["\'2020/10/10\' does not match \'^\\\\\\\\d{4}\\\\\\\\-\\\\\\\\d{2}\\\\\\\\-\\\\\\\\d{2}$\'"]')

    def test_report_detial_return_empty(self):
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'type': 'Energy', 'date': '2020-10-10'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[]')

    @freeze_time("2012-01-14")
    def test_report_detial_return_correctly(self):
        mommy.make(Plant, id=1)
        mommy.make(Report, plant_id=1, type='Energy', monitoring_date=datetime.now(),
                   expected=2.0, observed=2.0, date_created=datetime.now())
        response = self.client.get(resolve_url('report_detail'),
                                   {'plant_id': '1', 'type': 'Energy', 'date': '2012-01-14'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[{"plant":1,"type":"Energy","expected":2.0,"observed":2.0,"date_created":"2012-01-14T00:00:00Z","monitoring_date":"2012-01-14T00:00:00Z"}]')


class TestMonitoringView(TestCase):

    def setUp(self) -> None:
        self.command_mock = mock.patch('app.views.call_command').start()

    def tearDown(self) -> None:
        mock.patch.stopall()

    def test_validate_plant_parameter_required(self):
        response = self.client.post(resolve_url('plant_data_monitoring'), {'date_end': '2020-01-01', 'date_start': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'plant\' is a required property"]')

    def test_validate_date_start_parameter_required(self):
        response = self.client.post(resolve_url('plant_data_monitoring'),
                                   {'plant': 'test', 'date_end': '2020-01-01', })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'date_start\' is a required property"]')

    def test_validate_date_start_parameter_correct_type(self):
        response = self.client.post(resolve_url('plant_data_monitoring'),
                                   {'plant': '1', 'date_end': '2020-01-01', 'date_start': '2020/01/01' })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'2020/01/01\' does not match \'^\\\\\\\\d{4}\\\\\\\\-\\\\\\\\d{2}\\\\\\\\-\\\\\\\\d{2}$\'"]')

    def test_validate_date_end_parameter_required(self):
        response = self.client.post(resolve_url('plant_data_monitoring'),
                                   {'plant': '1',  'date_start': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["\'date_end\' is a required property"]')

    def test_validate_date_end_parameter_correct_format(self):
        response = self.client.post(resolve_url('plant_data_monitoring'),
                                   {'plant': '1', 'date_end': '2020/10/10', 'date_start': '2020-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         '["\'2020/10/10\' does not match \'^\\\\\\\\d{4}\\\\\\\\-\\\\\\\\d{2}\\\\\\\\-\\\\\\\\d{2}$\'"]')

    def test_validate_date_start_less_than_date_end(self):
        response = self.client.post(resolve_url('plant_data_monitoring'), {'plant' : 'test',
                                                                           'date_end': '2020-01-01',
                                                                           'date_start': '2020-02-01'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), '["Date start must be less than date end"]')

    def test_validate_plant_exists(self):
        response = self.client.post(resolve_url('plant_data_monitoring'), {'plant': 'test',
                                                                           'date_end': '2020-02-01',
                                                                           'date_start': '2020-01-01'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode('utf-8'),'{"detail":"Plant test does not exists"}')

    def test_command_called(self):
        mommy.make(Plant, name='test')
        response = self.client.post(resolve_url('plant_data_monitoring'), {'plant': 'test',
                                                                           'date_end': '2020-02-01',
                                                                           'date_start': '2020-01-01'})

        self.command_mock.assert_called_once_with('pull_data', fromdate='2020-01-01', name='test', todate='2020-02-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),'{"message":"Data for Plant:test, between dates: 2020-01-01 and 2020-02-01 was sent to process."}')
