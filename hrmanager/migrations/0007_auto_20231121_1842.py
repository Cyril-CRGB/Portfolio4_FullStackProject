# Generated by Django 3.2.23 on 2023-11-21 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0006_auto_20231102_0712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary_items',
            options={'ordering': ['validity_year']},
        ),
        migrations.AddField(
            model_name='salary_items',
            name='validity_year',
            field=models.CharField(default='', max_length=4, unique=True),
        ),
    ]
