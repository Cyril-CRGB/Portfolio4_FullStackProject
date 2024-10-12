from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Validator to check if end date is earlier than start date
def validate_enddate(start_date, end_date):
    # Checking that end date cannot be earlier than start date
    if end_date and start_date and end_date < start_date:
        raise ValidationError('End date cannot be earlier than start date.')

# Validator for Social Security Number field
def validate_social_security_number(value):
    if len(value) != 13 or not value.isdigit():
        raise ValidationError('Social Security Number must be 13 digits.')

# Validator for email format
def validate_emailaddress(value):
    if not value.endswith('@example.com'):
        raise forms.ValidationError("Email must end with @example.com")

# Validator for alphabetic names
validate_alphabetics = RegexValidator(regex=r'^[a-zA-Z]+$', message="Only alphabetic characteres are allowed.")


