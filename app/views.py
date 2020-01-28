from django.core.management import call_command
from jsonschema import validate, ValidationError as SchemaError
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Plant, Report
from app.schemas import report_schema, monitoring_schema
from app.serializers import PlantSerializer, ReportSerializer


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


@api_view(['POST'])
def monitoring(request):
    try:
        validate(request.data, schema=monitoring_schema)

        date_start = request.data['date_start']
        date_end = request.data['date_end']
        if date_start > date_end:
            raise ValidationError(detail='Date start must be less than date end')

        plant_name = request.data['plant']
        plant = Plant.objects.get(name=plant_name)

        opt = {'name': plant.name,
               'fromdate': date_start,
               'todate': date_end, }

        call_command('pull_data', **opt)

        return Response({'message': f"Data for Plant:{plant_name}, between dates: "
                                    f"{date_start} and {date_end} was sent to process."})
    except SchemaError as e:
        raise ValidationError(detail=e.message)
    except Plant.DoesNotExist:
        raise NotFound(detail=f"Plant {plant_name} does not exists")
    except Exception as e:
        raise e

