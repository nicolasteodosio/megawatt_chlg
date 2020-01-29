from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time
from model_mommy import mommy

from app.models import Plant, Report
from app.tasks import save_monitor_data


class TestSaveMonitorData(TestCase):

    def test_save_monitor_data_only_create(self):
        mommy.make(Plant, id=4)

        self.assertFalse(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 0)

        save_monitor_data(plant_id=4, msg={
            "datetime": "2019-01-01T00:00:00",
            "expected": {
                "energy": 16.483056690073553,
                "irradiation": 45.01428072656522
            },
            "observed": {
                "energy": 6.027445716078263,
                "irradiation": 24.212209652011897
            }
        })
        self.assertTrue(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 2)

    @freeze_time("2020-10-10")
    def test_save_monitor_data_update_only(self):
        mommy.make(Plant, id=4)
        mommy.make(Report, plant_id=4, type='Energy', expected=0.1, observed=0.3, monitoring_date=datetime.now())
        mommy.make(Report, plant_id=4, type='Irradiation', expected=0.1, observed=0.3, monitoring_date=datetime.now())

        self.assertTrue(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 2)
        self.assertEqual(Report.objects.get(plant_id=4, type='Energy', monitoring_date=datetime.now()).expected, 0.1)

        save_monitor_data(plant_id=4, msg={
            "datetime": "2020-10-10T00:00:00",
            "expected": {
                "energy": 16.4,
                "irradiation": 45.01
            },
            "observed": {
                "energy": 6.02,
                "irradiation": 24.2
            }
        })
        self.assertTrue(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 2)
        self.assertEqual(Report.objects.get(plant_id=4, type='Energy', monitoring_date=datetime.now()).expected, 16.4)

    @freeze_time("2020-10-10")
    def test_save_monitor_data_update_and_create(self):
        mommy.make(Plant, id=4)
        mommy.make(Report, plant_id=4, type='Energy', expected=0.1, observed=0.3, monitoring_date=datetime.now())

        self.assertTrue(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 1)
        self.assertEqual(Report.objects.get(plant_id=4, type='Energy', monitoring_date=datetime.now()).expected, 0.1)

        save_monitor_data(plant_id=4, msg={
            "datetime": "2020-10-10T00:00:00",
            "expected": {
                "energy": 16.4,
                "irradiation": 45.01
            },
            "observed": {
                "energy": 6.02,
                "irradiation": 24.2
            }
        })
        self.assertTrue(Report.objects.filter(plant_id=4).exists())
        self.assertEqual(Report.objects.filter(plant_id=4).count(), 2)
        self.assertEqual(Report.objects.get(plant_id=4, type='Energy', monitoring_date=datetime.now()).expected, 16.4)