from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Active"), (1, "Inactive"))
EMPLOYEES_GENDER = [
    ("F", "Female"),
    ("M", "Male"),
    ("O", "Other"),
]
EMPLOYEES_MARITAL_STATUS = [
    ("M", "Married"),
    ("D", "Divorced"),
    ("S", "Single"),
    ("P", "Partnership"),
    ("O", "Other"),
]
CHILDREN_BELOW_18 = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),  # to be corrected
]
CHILDREN_BELOW_25 = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),  # to be corrected
]


class Employees(models.Model):
    # basic personal information
    title = models.CharField(max_length=200, unique=True, default='')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    employees_gender = models.CharField(max_length=1, choices=EMPLOYEES_GENDER)
    employees_marital_status = models.CharField(
        max_length=1, choices=EMPLOYEES_MARITAL_STATUS)
    children_for_allocations_type_1 = models.CharField(
        choices=CHILDREN_BELOW_18, blank=True, max_length=2)
    children_for_allocations_type_2 = models.CharField(
        choices=CHILDREN_BELOW_25, blank=True, max_length=2)
    birth_date = models.DateField()
    employees_age = models.PositiveSmallIntegerField()
    email_adress = models.EmailField()
    phone_number = models.IntegerField()
    emergency_contact = models.CharField(max_length=30)
    emergency_phonenumber = models.IntegerField()
    employee_picture = CloudinaryField('image', default='placeholder')
    social_security_number = models.CharField(
        max_length=13, unique=True)
    employees_bankaccount = models.CharField(max_length=21)
    # basic salary information
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    employees_holiday_rights = models.IntegerField()
    base_monthly_salary = models.IntegerField()
    employees_phone_allocation = models.PositiveSmallIntegerField()
    employees_representation_allocation = models.PositiveSmallIntegerField()
    # basic calculated information
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    seniority = models.DurationField()
    # status
    employees_status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['start_date']
        unique_together = [['first_name', 'last_name']]

    def __str__(self):
        return self.title


class salary_items(models.Model):
    # constant variables for automatic calculation
    avs_item = models.DecimalField(max_digits=4, decimal_places=2)
    ac_item = models.DecimalField(max_digits=4, decimal_places=2)
    ac2_item = models.DecimalField(max_digits=4, decimal_places=2)
    laap_item = models.DecimalField(max_digits=4, decimal_places=2)
    laanp_item = models.DecimalField(max_digits=4, decimal_places=2)
    laac_item = models.DecimalField(max_digits=4, decimal_places=2)
    laace_item = models.DecimalField(max_digits=4, decimal_places=2)
    amat_item = models.DecimalField(max_digits=4, decimal_places=2)
    alfa_item = models.DecimalField(max_digits=4, decimal_places=2)
    apgmal_item = models.DecimalField(max_digits=4, decimal_places=2)
    alpetiteenfance_item = models.DecimalField(max_digits=4, decimal_places=2)
    # temporary variables for manual entries
    expense_report = models.DecimalField(max_digits=5, decimal_places=2)
    public_transportation_fees = models.DecimalField(
        max_digits=6, decimal_places=2)
