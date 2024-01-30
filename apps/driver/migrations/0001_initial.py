# Generated by Django 4.2.5 on 2024-01-30 12:11

import api.utils.image
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('ssn', models.CharField(blank=True, max_length=255, null=True, verbose_name='SSN')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State')),
                ('zip_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Zip')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Emergency Phone')),
                ('second_driver', models.BooleanField(default=False, verbose_name='Second Driver (team)')),
                ('lisense_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Lisense Number')),
                ('lisense_state', models.CharField(blank=True, max_length=255, null=True, verbose_name='Lisense State')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Type')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='Expiration Date')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Avatar')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vehicle_type', models.CharField(choices=[('CARGO VAN', 'CARGO VAN'), ('SPRINTER VAN', 'SPRINTER VAN'), ('VAN', 'VAN'), ('SPRINTER', 'SPRINTER'), ('BOX TRUCK', 'BOX TRUCK'), ('SMALL STRAIGHT', 'SMALL STRAIGHT'), ('LARGE STRAIGHT', 'LARGE STRAIGHT'), ('LIFTGATE', 'LIFTGATE'), ('FLATBED', 'FLATBED'), ('TRACTOR', 'TRACTOR'), ('REEFER', 'REEFER')], default='SPRINTER VAN', max_length=100, null=True, verbose_name='vehicle')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
                'ordering': ('-id',),
            },
            bases=(models.Model, api.utils.image.ImageService),
        ),
    ]
