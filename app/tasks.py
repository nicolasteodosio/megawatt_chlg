from datetime import datetime, timedelta

from django.core.management import call_command

from app.models import Report, Plant
from megawatt.celery import app


@app.task(bind=True)
def save_monitor_data(self, plant_id, msg):
    try:

        dict_to_create = {'datetime': msg['datetime'],
                          'energy': {'expected': msg['expected']['energy'], 'observed': msg['observed']['energy']},
                          'irradiation': {'irradiation': msg['expected']['irradiation'],
                                          'observed': msg['observed']['irradiation'], }
                          }
        Report.objects.update_or_create(
            monitoring_date=dict_to_create['datetime'],
            plant_id=plant_id, type=Report.TypesChoices.energy,
            defaults={'expected': dict_to_create['energy']['expected'],
                      'observed': dict_to_create['energy']['observed'], })

        Report.objects.update_or_create(
            monitoring_date=dict_to_create['datetime'],
            plant_id=plant_id, type=Report.TypesChoices.irradiation,
            defaults={'expected': dict_to_create['energy']['expected'],
                      'observed': dict_to_create['energy']['observed'], })

    except Exception as e:
        raise self.retry(exc=e)


@app.task(bind=True)
def daily_get_plants_monitor_data(self):
    try:
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        for plant in Plant.objects.all():
            params = {'name': plant.name,
                      'fromdate': yesterday,
                      'todate': today,
                      }

            call_command('pull_data', **params)
    except Exception as e:
        raise self.retry(exc=e)
