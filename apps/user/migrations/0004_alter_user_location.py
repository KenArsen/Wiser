# Generated by Django 4.2.5 on 2023-11-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0003_alter_user_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
