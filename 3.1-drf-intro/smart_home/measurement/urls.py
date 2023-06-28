from django.urls import path

from measurement.views import SensorListCreateAPIView, SensorRetrieveUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    path('sensors/', SensorListCreateAPIView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdateAPIView.as_view()),
    path('measurements/', MeasurementCreateAPIView.as_view()),
]
