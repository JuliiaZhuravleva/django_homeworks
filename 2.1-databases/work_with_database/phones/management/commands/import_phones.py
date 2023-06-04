import csv
from tempfile import NamedTemporaryFile

import requests
from datetime import datetime

from django.core.files import File
from django.core.management.base import BaseCommand

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            image_url = phone['image']
            image_response = requests.get(image_url)
            image_name = image_url.split('/')[-2]

            with NamedTemporaryFile(delete=True) as image_file:
                image_file.write(image_response.content)

                phone_obj = Phone(
                    id=phone['id'],
                    image=File(image_file, name=image_name),
                    name=phone['name'],
                    price=phone['price'],
                    release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d'),
                    lte_exists=phone['lte_exists'],
                    slug=phone['name'].lower().replace(' ', '-')
                )
                phone_obj.save()


