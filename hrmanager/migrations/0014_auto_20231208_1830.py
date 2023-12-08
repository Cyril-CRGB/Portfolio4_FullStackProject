# Generated by Django 3.2.22 on 2023-12-08 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrmanager', '0013_auto_20231128_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='base_monthly_salary',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='email_adress',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='emergency_phonenumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employees_age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employees_bankaccount',
            field=models.CharField(blank=True, max_length=21, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employees_holiday_rights',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='seniority',
            field=models.DurationField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='generatordata',
            name='gd_monthly_table_paid',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
    ]