# Generated by Django 4.2.10 on 2024-05-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_transit_distance_order_transit_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('AWAITING_BID', 'AWAITING BID'), ('REFUSED', 'REFUSED'), ('ASSIGNED', 'ASSIGNED'), ('CHECKOUT', 'CHECKOUT'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED'), ('EXPIRED', 'EXPIRED')], default='PENDING', max_length=100),
        ),
    ]
