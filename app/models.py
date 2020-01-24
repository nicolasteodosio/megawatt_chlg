from django.db import models


class Plant(models.Model):
    name = models.CharField('Name', max_length=75)


class Datapoint(models.Model):
    plant_id = models.ForeignKey(Plant, on_delete=models.DO_NOTHING)
    energy_expected = models.FloatField('Expected energy')
    energy_observed = models.FloatField('Observed energy')
    irradiation_observed = models.FloatField('Observed irradiation')
    irradiation_expected = models.FloatField('Expected irradiation')
