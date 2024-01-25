# Generated by Django 4.2.5 on 2023-11-24 04:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_whom', models.EmailField(blank=True, max_length=254, null=True)),
                ('pick_up_at', models.CharField(blank=True, max_length=255, null=True)),
                ('pick_up_date_CEN', models.DateTimeField(blank=True, null=True)),
                ('pick_up_date_EST', models.DateTimeField(blank=True, null=True)),
                ('deliver_to', models.CharField(blank=True, max_length=255, null=True)),
                ('deliver_date_CEN', models.DateTimeField(blank=True, null=True)),
                ('deliver_date_EST', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=400, null=True)),
                ('miles', models.FloatField(blank=True, null=True)),
                ('pieces', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('dims', models.CharField(blank=True, max_length=255, null=True)),
                ('stackable', models.CharField(blank=True, max_length=255, null=True)),
                ('hazardous', models.CharField(blank=True, max_length=255, null=True)),
                ('fast_load', models.CharField(blank=True, max_length=255, null=True)),
                ('dock_level', models.CharField(blank=True, max_length=255, null=True)),
                ('suggested_truck_size', models.CharField(blank=True, max_length=255, null=True)),
                ('this_posting_expires_cen', models.DateTimeField(blank=True, null=True)),
                ('this_posting_expires_est', models.DateTimeField(blank=True, null=True)),
                ('load_posted_by', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
                ('order_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
