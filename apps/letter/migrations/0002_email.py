# Generated by Django 4.2.5 on 2024-01-31 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
