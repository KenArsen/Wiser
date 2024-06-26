# Generated by Django 4.2.10 on 2024-04-18 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit_id', models.CharField(max_length=255)),
                ('transport_type', models.CharField(choices=[('CARGO VAN', 'CARGO VAN'), ('SPRINTER VAN', 'SPRINTER VAN'), ('VAN', 'VAN'), ('SPRINTER', 'SPRINTER'), ('BOX TRUCK', 'BOX TRUCK'), ('SMALL STRAIGHT', 'SMALL STRAIGHT'), ('LARGE STRAIGHT', 'LARGE STRAIGHT'), ('LIFTGATE', 'LIFTGATE'), ('FLATBED', 'FLATBED'), ('TRACTOR', 'TRACTOR'), ('REEFER', 'REEFER')], default='SPRINTER VAN', max_length=255)),
                ('vehicle_model', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle_year', models.CharField(blank=True, max_length=255, null=True)),
                ('dock_high', models.BooleanField(default=False)),
                ('width', models.IntegerField(blank=True, default=0, null=True)),
                ('height', models.IntegerField(blank=True, default=0, null=True)),
                ('length', models.IntegerField(blank=True, default=0, null=True)),
                ('payload', models.IntegerField(blank=True, default=0, null=True)),
                ('vin', models.CharField(blank=True, max_length=255, null=True)),
                ('lisense_plate', models.CharField(blank=True, max_length=255, null=True)),
                ('lisense_plate_state', models.CharField(blank=True, max_length=255, null=True)),
                ('lisense_expiry_date', models.CharField(blank=True, max_length=255, null=True)),
                ('lisense_expiry_state', models.CharField(blank=True, max_length=255, null=True)),
                ('dispatcher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dispatcher_vehicles', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_vehicles', to='driver.driver')),
                ('vehicle_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_vehicles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
