# Generated by Django 4.2.5 on 2023-11-29 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('read_email', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
