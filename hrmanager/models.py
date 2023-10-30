from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "active"), (1, "inactive"))


class Employees(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    EMPLOYEES_GENDER = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other"),
    ]
    employees_gender = models.CharField(max_length=1, choices=EMPLOYEES_GENDER)

    EMPLOYEES_MARITAL_STATUS = [
        ("M", "Married"),
        ("D", "Divorced"),
        ("S", "Single"),
        ("P", "Partnership"),
        ("O", "Other"),
    ]
    employees_marital_status = models.CharField(
        max_length=1, choices=EMPLOYEES_MARITAL_STATUS)

    ChildrenBelow18 = models.IntegerChoices(
        "Number of children below 18", 0 1 2 3 4 5 6 7 8 9 10)
    children_for_allocations_type_1 = models.IntegerField(
        choices=ChildrenBelow18.choices)
    ChildrenBelow25 = models.IntegerChoices(
        "Number of children below 25 still studying", 0 1 2 3 4 5 6 7 8 9 10)
    children_for_allocations_type_2 = models.IntegerField(
        choices=ChildrenBelow25.choices)

    start_date = models.DateField()
    end_date = models.DateField()
    birth_date = models.DateField()
    employees_age = models.PositiveSmallIntegerField()
    email_adress = models.EmailField()
    phone_number = models.IntegerField()
    emergency_contact = models.CharField()
    emergency_phonenumber = models.IntegerField()
    employee_picture = models.ImageField()
    social_security_number = models.PositiveBigIntegerField()
    base_monthly_salary = models.IntegerField()

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    seniority = models.DurationField()
