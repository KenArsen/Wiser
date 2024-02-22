# Generated by Django 4.2.10 on 2024-02-22 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_order_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='created',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('DEFAULT', '----'), ('PENDING', 'Pending'), ('A', 'Выехал на точку А'), ('B', 'Загрузил'), ('C', 'В дороге'), ('D', 'Выгрузил')], default='DEFAULT', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
