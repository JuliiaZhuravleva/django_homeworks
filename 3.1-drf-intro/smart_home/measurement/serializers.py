from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from measurement.models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Measurement
        fields = ['id', 'temperature', 'created_at', 'sensor', 'image']


class MeasurementShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementShortSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']


class SensorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']
