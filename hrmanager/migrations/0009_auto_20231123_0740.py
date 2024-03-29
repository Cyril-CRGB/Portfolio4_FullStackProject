# Generated by Django 3.2.23 on 2023-11-23 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0008_generatordata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatordata',
            name='gd_base_monthly_salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_child_allocation_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_child_allocation_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_total_monthly_wage',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_total_monthly_wage_for_social_insurance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_total_monthly_wage_for_social_taxes',
            field=models.IntegerField(default=0),
        ),
    ]
