# Generated by Django 4.2.10 on 2024-05-02 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='broker_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='letter',
            name='driver_price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
