from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Sensor, Measurement


class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 0


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    inlines = [MeasurementInline]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'created_at', 'sensor']
