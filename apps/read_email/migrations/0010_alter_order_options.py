# Generated by Django 4.2.5 on 2023-12-19 19:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('read_email', '0009_rename_contact_info_order_company_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
    ]