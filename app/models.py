from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class Plant(models.Model):
    name = models.CharField('Name', max_length=75)


class Report(models.Model):

    class TypesChoices(DjangoChoices):
        energy = ChoiceItem('Energy')
        irradiation = ChoiceItem('Irradiation')

    plant_id = models.ForeignKey(Plant, on_delete=models.DO_NOTHING)
    type = models.CharField('Type of report', choices=TypesChoices.choices, max_length=15)
    expected = models.FloatField('Expected')
    observed = models.FloatField('Observed')
