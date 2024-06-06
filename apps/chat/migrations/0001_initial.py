# Generated by Django 4.2.10 on 2024-06-04 05:20

import apps.chat.models.group_model
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.chat.models.group_model.get_image_path)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_groups', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='chat_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.chat.models.group_model.get_file_path)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.group')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
