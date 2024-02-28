# Generated by Django 4.2.10 on 2024-02-24 09:18

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliver_date_CEN',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 24, 10, 18, 14, 424860, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliver_date_EST',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 24, 10, 18, 14, 424877, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='pick_up_date_CEN',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='pick_up_date_EST',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='this_posting_expires_cen',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 24, 9, 28, 14, 424950, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='this_posting_expires_est',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 24, 9, 28, 14, 424959, tzinfo=datetime.timezone.utc)),
        ),
    ]