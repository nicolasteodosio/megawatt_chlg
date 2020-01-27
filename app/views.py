from jsonschema import validate, ValidationError as SchemaError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from app.models import Plant, Report
from app.schemas import report_schema
from app.serializers import PlantSerializer, ReportSerializer
from rest_framework import generics


class PlantList(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class ReportDetail(APIView):

    def get(self, request):
        try:
            validate(request.GET, schema=report_schema)

            reports = Report.objects.filter(plant_id=request.GET.get('plant_id'), type=request.GET.get('type'),
                                            monitoring_date__contains=request.GET.get('date'))
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data)
        except SchemaError as e:
            raise ValidationError(detail=e.message)
        except Exception as e:
            raise e
