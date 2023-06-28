# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorShortSerializer


class SensorListCreateAPIView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorShortSerializer


class SensorRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementCreateAPIView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
