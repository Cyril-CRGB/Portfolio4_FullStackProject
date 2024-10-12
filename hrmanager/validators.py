from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import timedelta, date
import datetime

# Validator to check if end date is earlier than start date
def validate_enddate(start_date, end_date):
    # Checking that end date cannot be earlier than start date
    if end_date and start_date and end_date < start_date:
        raise ValidationError('End date cannot be earlier than start date.')

# Validator for Social Security Number field
def validate_social_security_number(value):
    if len(value) != 13 or not value.isdigit():
        raise ValidationError('Social Security Number must be 13 digits.')

# Validator for alphabetic names
validate_alphabetics = RegexValidator(regex=r'^[a-zA-Z]+$', message="Only alphabetic characteres are allowed.")

# Validator for birth date
def validate_birth_date_in_past(value):
    if value > date.today():
        raise ValidationError('Birth date cannot be in the future.')

# Validator for age
def validate_age_and_date_birth(age, birth_date):
    # Check if age or birth_date is None or blank
    if not age or not birth_date:
        raise ValidationError("Both age and birth date must be provided.")
    today = date.today()
    y = (today.year - birth_date.year) - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age != y:
        raise ValidationError("The age given does not match date of birth.")

# Validator to ensure phone number follows the format 0041/00.000.00.00
validate_phone_number_format = RegexValidator(regex=r'^0041/\d{2}\.\d{3}\.\d{2}\.\d{2}$', message="Phone number must be in the format 00041/00.000.00.00")

# Validator to ensure employees_bankaccount follows the format CH00 0000 0000 0000 0000 0
validate_employees_bankaccount_format = RegexValidator(regex=r'^CH\d{2} \d{4} \d{4} \d{4} \d{4} \d{1}$', message="Bank account number must be in the format CH00 0000 0000 0000 0000 0")

# Validator to ensure DateField format
def validate_date_format(value):
    if not isinstance(value, datetime.date):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError("Date must be in the format YYYY-MM-DD")
    else:
        # Value is already a date object, so no need to parse it again
        pass

# Validator that ensure value is not blank or null
def validate_not_blank_nor_null(value):
    if value is None or value =='':
        raise ValidationError('This field cannot be null nor blank.')




