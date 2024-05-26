# Generated by Django 4.2.10 on 2024-05-22 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0007_alter_vehicles_coordinate_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='payload',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='transport_type',
            field=models.CharField(choices=[('CARGO VAN', 'Cargo Van'), ('SPRINTER VAN', 'Sprinter Van'), ('VAN', 'Van'), ('SPRINTER', 'Sprinter'), ('BOX TRUCK', 'Box Truck'), ('SMALL STRAIGHT', 'Small Straight'), ('LARGE STRAIGHT', 'Large Straight'), ('LIFTGATE', 'Liftgate'), ('FLATBED', 'Flatbed'), ('TRACTOR', 'Tractor'), ('REEFER', 'Reefer')], default='SPRINTER VAN', max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='width',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]