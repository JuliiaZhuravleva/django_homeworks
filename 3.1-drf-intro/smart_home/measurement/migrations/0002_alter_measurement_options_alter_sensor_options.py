# Generated by Django 4.2.2 on 2023-06-27 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='sensor',
            options={'ordering': ['id']},
        ),
    ]