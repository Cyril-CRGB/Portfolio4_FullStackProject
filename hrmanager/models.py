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
    end_date = models.DateField(blank=True, null=True, default=None)
    employees_holiday_rights = models.IntegerField()
    base_monthly_salary = models.IntegerField()
    LPP_deduction_employee = models.IntegerField(
        blank=True, null=True, default=0)
    LPP_deduction_employer = models.IntegerField(
        blank=True, null=True, default=0)
    employees_phone_allocation = models.PositiveSmallIntegerField(
        blank=True, null=True, default=0)
    employees_representation_allocation = models.PositiveSmallIntegerField(
        blank=True, null=True, default=0)
    # temporary variables for manual entries --> should be in Employees model
    expense_report = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    public_transportation_fees = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    extraordinary_salary = models.IntegerField(
        blank=True, null=True, default=0)
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
    validity_year = models.CharField(max_length=4, unique=True, default='')
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
    child_alloc_1_item = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    child_alloc_2_item = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        ordering = ['validity_year']

    def __str__(self):
        return self.validity_year


class GeneratorData(models.Model):
    gd_year = models.IntegerField()
    gd_month = models.CharField(max_length=20)
    gd_title = models.CharField(max_length=255)
    gd_first_name = models.CharField(max_length=255)
    gd_last_name = models.CharField(max_length=255)
    gd_start_date = models.DateField(blank=True, null=True)
    gd_end_date = models.DateField(blank=True, null=True, default=None)
    gd_first_day_of_the_month_date = models.DateField(blank=True, null=True)
    gd_last_day_of_the_month_date = models.DateField(blank=True, null=True)
    gd_worked_days = models.IntegerField(default=0)
    gd_base_monthly_salary = models.IntegerField(default=0)
    gd_calculated_monthly_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    gd_child_allocation_1 = models.IntegerField(default=0)
    gd_child_allocation_2 = models.IntegerField(default=0)
    gd_total_monthly_wage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_total_monthly_wage_for_social_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_total_monthly_wage_for_social_taxes = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_avs_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_ac_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_ac2_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_laap_item = models.DecimalField(
        max_digits=4, decimal_places=2, default=0)
    gd_laanp_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_laac_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_laace_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_amat_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_alfa_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_apgmal_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_alpetiteenfance_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_total_social_deduction = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_employees_phone_allocation = models.PositiveSmallIntegerField(default=0)
    gd_employees_representation_allocation = models.PositiveSmallIntegerField(
        default=0)
    gd_expense_report = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_public_transportation_fees = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_paid_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_monthly_table_saved = models.DateTimeField(auto_now_add=True)
    gd_monthly_table_paid = models.DateTimeField(
        blank=True, null=True, default=None)
