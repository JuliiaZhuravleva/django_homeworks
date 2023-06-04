from django.db import models


class Phone(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='static/uploads/')
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()
