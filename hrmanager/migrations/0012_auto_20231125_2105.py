# Generated by Django 3.2.23 on 2023-11-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0011_auto_20231124_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatordata',
            name='gd_monthly_table_paid',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='generatordata',
            name='gd_monthly_table_saved',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
