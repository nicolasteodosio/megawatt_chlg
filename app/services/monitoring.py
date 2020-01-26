from django.conf import settings

from app.utils import requests_retry_session


class MonitoringService:

    def __init__(self, plant, start_date, end_date) -> None:
        self.plant = plant
        self.start_date = start_date
        self.end_date = end_date

    def pull_data(self):
        try:
            response = requests_retry_session().get(f'{settings.MONITORING_URL}/?plant-id={self.plant}&'
                                                    f'from={self.start_date}&to={self.end_date}')
            return response.json()
        except Exception as e:
            raise e
