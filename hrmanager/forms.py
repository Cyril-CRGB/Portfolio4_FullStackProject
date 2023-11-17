from django import forms
from .models import Employees


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['title', 'first_name', 'last_name', 'employees_gender',
                  'employees_marital_status', 'children_for_allocations_type_1', 'children_for_allocations_type_2',
                  'birth_date', 'employees_age', 'email_adress', 'phone_number', 'emergency_contact', 'emergency_phonenumber',
                  'employee_picture', 'social_security_number', 'employees_bankaccount', 'start_date', 'end_date',
                  'employees_holiday_rights', 'base_monthly_salary', 'employees_phone_allocation',
                  'employees_representation_allocation', 'seniority', 'employees_status']
