# Generated by Django 3.2.22 on 2023-11-02 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0004_alter_employees_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='title',
            field=models.CharField(default='full name', max_length=200, unique=True),
        ),
    ]