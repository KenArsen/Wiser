# Generated by Django 4.2.10 on 2024-04-22 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_vehicles_coordinate_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='coordinate_from',
            field=models.CharField(default='40.730610, -73.935242', max_length=255),
        ),
    ]
