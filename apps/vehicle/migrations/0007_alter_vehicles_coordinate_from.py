# Generated by Django 4.2.10 on 2024-05-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0006_alter_vehicles_coordinate_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='coordinate_from',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
