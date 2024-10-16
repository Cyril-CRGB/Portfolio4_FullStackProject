# Importing the necessary modules or classes
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .validators import validate_alphabetics, validate_social_security_number, validate_enddate, validate_birth_date_in_past, validate_phone_number_format, validate_employees_bankaccount_format, validate_date_format, validate_age_and_date_birth, validate_not_blank_nor_null
from datetime import timedelta, date

# Status choices for employees
STATUS = ((0, "Active"), (1, "Inactive"))

# Choices for gender
EMPLOYEES_GENDER = [
    ("F", "Female"),
    ("M", "Male"),
    ("O", "Other"),
]

# Choices for marital status
EMPLOYEES_MARITAL_STATUS = [
    ("M", "Married"),
    ("D", "Divorced"),
    ("S", "Single"),
    ("P", "Partnership"),
    ("O", "Other"),
]

# Choice for the number of children below 18
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
    ("10", "10"),
]

# Choice for the number of children below 25
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
    ("10", "10"),
]


class Employees(models.Model):
    # basic personal information
    title = models.CharField(max_length=200, unique=True, default='', error_messages={'unique': "An employee with this title already exists."})
    first_name = models.CharField(max_length=30, null=False, blank=False, validators=[validate_alphabetics, validate_not_blank_nor_null])
    last_name = models.CharField(max_length=30, null=False, blank=False, validators=[validate_alphabetics, validate_not_blank_nor_null])
    employees_gender = models.CharField(max_length=1, choices=EMPLOYEES_GENDER)
    employees_marital_status = models.CharField(
        max_length=1, choices=EMPLOYEES_MARITAL_STATUS)
    children_for_allocations_type_1 = models.CharField(
        choices=CHILDREN_BELOW_18, blank=True, max_length=2, validators=[validate_not_blank_nor_null])
    children_for_allocations_type_2 = models.CharField(
        choices=CHILDREN_BELOW_25, blank=True, max_length=2, validators=[validate_not_blank_nor_null])
    birth_date = models.DateField(blank=False, null=False, validators=[validate_birth_date_in_past, validate_date_format, validate_not_blank_nor_null], default=date.today)
    employees_age = models.PositiveSmallIntegerField(blank=False, null=False, validators=[validate_not_blank_nor_null], default='0')
    email_adress = models.EmailField(
        blank=False,
        null=False,
        validators=[validate_email, validate_not_blank_nor_null],
        unique=True,
        error_messages={
            'unique': "An employee with this email address already exists."
        },
        default='noneemail@noneemail.com'
    )
    phone_number = models.CharField(max_length=17, blank=True, null=True, validators=[validate_phone_number_format, validate_not_blank_nor_null], help_text="Format: 0041/00.000.00.00")
    emergency_contact = models.CharField(
        max_length=30, blank=True, null=True)
    emergency_phonenumber = models.CharField(max_length=17, blank=True, null=True, validators=[validate_phone_number_format], help_text="Format: 0041/00.000.00.00")
    employee_picture = CloudinaryField('image', default='placeholder')
    social_security_number = models.CharField(
        max_length=13, 
        validators=[validate_social_security_number, validate_not_blank_nor_null],
        unique=True,
        error_messages={
            'unique': "An employee with this Social Security Number already exists."
        }
    )
    employees_bankaccount = models.CharField(
        max_length=21, blank=True, null=True, validators=[validate_employees_bankaccount_format, validate_not_blank_nor_null], help_text="Format: CH00 0000 0000 0000 0000 0")
    # basic salary information
    start_date = models.DateField(blank=False, null=False, validators=[validate_not_blank_nor_null], default=date.today)
    end_date = models.DateField(blank=True, null=True, default='None')
    employees_holiday_rights = models.IntegerField(
        blank=True, null=True, default=0)
    base_monthly_salary = models.IntegerField(blank=True, null=True, default=0)
    LPP_deduction_employee = models.IntegerField(
        blank=True, null=True, default=0)
    LPP_deduction_employer = models.IntegerField(
        blank=True, null=True, default=0)
    employees_phone_allocation = models.PositiveSmallIntegerField(
        blank=False, null=False, default=0, validators=[validate_not_blank_nor_null])
    employees_representation_allocation = models.PositiveSmallIntegerField(
        blank=False, null=False, default=0, validators=[validate_not_blank_nor_null])
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
    seniority = models.DurationField(blank=True, null=True)
    # status
    employees_status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['start_date']
        unique_together = [['first_name', 'last_name']]

    # Method to validate relationships between multiple fields
    def clean(self):
        # Call the parent clean method
        super().clean()
        # Testing if End date comes before start date
        validate_enddate(self.start_date, self.end_date)
        # Testing if date of birth match age
        validate_age_and_date_birth(self.employees_age, self.birth_date)


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
    gd_monthly_salary = models.DecimalField(
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
    gd_monthly_table_saved = models.DateTimeField(
        auto_now_add=True)
    gd_monthly_table_paid = models.DateTimeField(
        blank=True, null=True, default=None, editable=False)
    gd_extraordinary_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_LPP_deduction_employee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_total_deduction_employee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gd_correction_non_financial_wage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
