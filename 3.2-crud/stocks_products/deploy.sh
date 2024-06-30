#!/bin/bash

cd /home/user/django_homeworks/3.2-crud/stocks_products
git pull origin master
source env/bin/activate
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart gunicorn
