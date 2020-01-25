from rest_framework import serializers

from app.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name']


class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'plant_id', 'energy_expected', 'energy_observed',
                  'irradiation_observed', 'irradiation_expected']
