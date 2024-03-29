# Generated by Django 4.2.3 on 2023-07-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_favouriteadvertisement_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favouriteadvertisement',
            name='unique combination',
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='status',
            field=models.TextField(choices=[('OPEN', 'Открыто'), ('CLOSED', 'Закрыто'), ('DRAFT', 'Черновик')], default='DRAFT'),
        ),
        migrations.AddConstraint(
            model_name='favouriteadvertisement',
            constraint=models.UniqueConstraint(fields=('user', 'advertisement'), name='unique_combination'),
        ),
    ]
