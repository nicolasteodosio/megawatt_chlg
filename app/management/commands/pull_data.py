import argparse
from datetime import datetime

from django.core.management import BaseCommand, CommandError

from app.models import Plant
from app.services.monitoring import MonitoringService


# Code extracted from: https://stackoverflow.com/questions/25470844/specify-format-for-input-arguments-argparse-python
def valid_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_string)
        raise argparse.ArgumentTypeError(msg)


class Command(BaseCommand):
    help = 'Pull data from the monitoring service'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True)
        parser.add_argument('--fromdate', help="The Start Date - format YYYY-MM-DD",
                            type=valid_date, required=True)
        parser.add_argument('--todate', help="The End Date - format YYYY-MM-DD",
                            type=valid_date, required=True)

    def handle(self, *args, **options):
        try:
            plant = Plant.objects.get(name=options['name'])
        except Plant.DoesNotExist:
            raise CommandError(f"Plant name={options['name']}, does not exist.")

        monitoring_service = MonitoringService(plant=plant.name, start_date=options['fromdate'],
                                               end_date=options['todate'])
        data = monitoring_service.pull_data()
        print(data)