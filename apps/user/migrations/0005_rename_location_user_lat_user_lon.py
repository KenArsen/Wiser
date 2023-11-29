# Generated by Django 4.2.5 on 2023-11-28 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='lat',
        ),
        migrations.AddField(
            model_name='user',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
