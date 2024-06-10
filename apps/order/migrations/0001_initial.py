# Generated by Django 4.2.10 on 2024-06-10 09:46

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
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='orders/logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('AWAITING_BID', 'AWAITING BID'), ('REFUSED', 'REFUSED'), ('ACTIVE', 'ACTIVE'), ('CHECKOUT', 'CHECKOUT'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED'), ('EXPIRED', 'EXPIRED')], default='PENDING', max_length=100)),
                ('order_number', models.PositiveIntegerField(blank=True, null=True)),
                ('pick_up_location', models.CharField(blank=True, max_length=255, null=True)),
                ('pick_up_latitude', models.FloatField(blank=True, null=True)),
                ('pick_up_longitude', models.FloatField(blank=True, null=True)),
                ('pick_up_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_location', models.CharField(blank=True, max_length=255, null=True)),
                ('delivery_latitude', models.FloatField(blank=True, null=True)),
                ('delivery_longitude', models.FloatField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('stops', models.CharField(blank=True, max_length=255, null=True)),
                ('broker', models.CharField(blank=True, max_length=255, null=True)),
                ('broker_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('broker_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('posted_date', models.DateTimeField(blank=True, null=True)),
                ('expires_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('dock_level', models.BooleanField(default=False)),
                ('hazmat', models.BooleanField(default=False)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('fast_load', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, max_length=400, null=True)),
                ('load_type', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle_required', models.CharField(blank=True, max_length=255, null=True)),
                ('pieces', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('weight', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('dimensions', models.CharField(blank=True, max_length=255, null=True)),
                ('stackable', models.BooleanField(default=False)),
                ('match', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='MyLoadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('previous_status', models.PositiveSmallIntegerField(choices=[(1, 'I am going to the load'), (2, 'Uploaded'), (3, 'On the way'), (4, 'Unloaded'), (5, 'Delivered'), (6, 'Paid off'), (7, 'Completed')], null=True)),
                ('current_status', models.PositiveSmallIntegerField(choices=[(1, 'I am going to the load'), (2, 'Uploaded'), (3, 'On the way'), (4, 'Unloaded'), (5, 'Delivered'), (6, 'Paid off'), (7, 'Completed')], null=True)),
                ('next_status', models.PositiveSmallIntegerField(choices=[(1, 'I am going to the load'), (2, 'Uploaded'), (3, 'On the way'), (4, 'Unloaded'), (5, 'Delivered'), (6, 'Paid off'), (7, 'Completed')], null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_load_status', to='order.order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('broker_price', models.PositiveIntegerField(blank=True, null=True)),
                ('driver_price', models.PositiveIntegerField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters', to='driver.driver')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='letter', to='order.order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('broker_company', models.CharField(max_length=255)),
                ('rate_confirmation', models.CharField(max_length=255)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assign', to='order.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
