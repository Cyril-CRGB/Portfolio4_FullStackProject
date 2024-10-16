# Generated by Django 3.2.22 on 2024-10-12 21:38

import datetime
from django.db import migrations, models
import hrmanager.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0002_auto_20241012_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='birth_date',
            field=models.DateField(default=datetime.date.today, validators=[hrmanager.validators.validate_birth_date_in_past, hrmanager.validators.validate_date_format, hrmanager.validators.validate_not_blank_nor_null]),
        ),
        migrations.AlterField(
            model_name='employees',
            name='start_date',
            field=models.DateField(default=datetime.date.today, validators=[hrmanager.validators.validate_not_blank_nor_null]),
        ),
    ]
