# Generated by Django 4.2.5 on 2023-11-24 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(choices=[('CARGO VAN', 'CARGO VAN'), ('SPRINTER VAN', 'SPRINTER VAN'), ('VAN', 'VAN'), ('SPRINTER', 'SPRINTER'), ('BOX TRUCK', 'BOX TRUCK'), ('SMALL STRAIGHT', 'SMALL STRAIGHT'), ('LARGE STRAIGHT', 'LARGE STRAIGHT'), ('LIFTGATE', 'LIFTGATE'), ('FLATBED', 'FLATBED'), ('TRACTOR', 'TRACTOR'), ('REEFER', 'REEFER')], default='SPRINTER VAN', max_length=100, null=True, verbose_name='vehicle'),
        ),
    ]