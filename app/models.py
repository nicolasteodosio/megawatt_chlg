from datetime import datetime

from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class Plant(models.Model):
    name = models.CharField('Name', max_length=75)

    def __str__(self):
        return self.name


class Report(models.Model):

    class TypesChoices(DjangoChoices):
        energy = ChoiceItem('Energy')
        irradiation = ChoiceItem('Irradiation')

    plant = models.ForeignKey(Plant, on_delete=models.DO_NOTHING)
    type = models.CharField('Type of report', choices=TypesChoices.choices, max_length=15)
    expected = models.FloatField('Expected')
    observed = models.FloatField('Observed')
    date_created = models.DateTimeField('Created date', auto_now_add=True)
    monitoring_date = models.DateTimeField('Monitoring date', default=datetime.now())

    def __str__(self):
        return '{} - {}'.format(self.plant_id, self.type)