# Generated by Django 3.2.22 on 2023-11-02 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0003_auto_20231102_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]