# Generated by Django 4.2.10 on 2024-04-22 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_vehicles_location_from_vehicles_location_from_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='coordinate_from',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
