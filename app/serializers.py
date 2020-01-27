from rest_framework import serializers

from app.models import Plant, Report


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['plant',
                  'type',
                  'expected',
                  'observed',
                  'date_created',
                  'monitoring_date']
