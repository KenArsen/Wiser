# Generated by Django 4.2.5 on 2023-11-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('read_email', '0003_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]