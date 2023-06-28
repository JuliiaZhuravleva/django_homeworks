from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.description})'


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/uploads/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Температура на {self.created_at}: {self.temperature}°C'
