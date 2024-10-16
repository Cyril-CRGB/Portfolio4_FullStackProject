from django import forms
from .models import Employees, salary_items, GeneratorData
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['title', 'first_name', 'last_name', 'employees_gender',
                  'employees_marital_status', 'children_for_allocations_type_1', 'children_for_allocations_type_2',
                  'birth_date', 'employees_age', 'email_adress', 'phone_number', 'emergency_contact', 'emergency_phonenumber',
                  'employee_picture', 'social_security_number', 'employees_bankaccount', 'start_date', 'end_date',
                  'employees_holiday_rights', 'base_monthly_salary', 'employees_phone_allocation',
                  'employees_representation_allocation', 'seniority', 'employees_status', 'expense_report',
                  'public_transportation_fees', 'LPP_deduction_employee', 'LPP_deduction_employer',
                  'extraordinary_salary']
    def clean(self):
        cleaned_data = super().clean() # This ensures the model clean() is called
        return cleaned_data


class ModifyEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['title', 'first_name', 'last_name', 'employees_gender',
                  'employees_marital_status', 'children_for_allocations_type_1', 'children_for_allocations_type_2',
                  'birth_date', 'employees_age', 'email_adress', 'phone_number', 'emergency_contact', 'emergency_phonenumber',
                  'employee_picture', 'social_security_number', 'employees_bankaccount', 'start_date', 'end_date',
                  'employees_holiday_rights', 'base_monthly_salary', 'employees_phone_allocation',
                  'employees_representation_allocation', 'seniority', 'employees_status', 'expense_report',
                  'public_transportation_fees', 'LPP_deduction_employee', 'LPP_deduction_employer',
                  'extraordinary_salary']
    def clean(self):
        cleaned_data = super().clean() # This ensures the model clean() is called
        return cleaned_data


class NewYearForm(forms.ModelForm):
    class Meta:
        model = salary_items
        fields = ['validity_year', 'avs_item', 'ac_item', 'ac2_item', 'laap_item',
                  'laanp_item', 'laac_item', 'laace_item',
                  'amat_item', 'alfa_item', 'apgmal_item', 'alpetiteenfance_item',
                  'child_alloc_1_item', 'child_alloc_2_item']
    def clean_validity_year(self):
        year = self.cleaned_data.get('validity_year')
        if not year.isdigit() or len(year) != 4:
            raise forms.ValidationError("The year must be a 4-digit number.")
        try:
            year = int(year)
        except ValueError:
            raise forms.ValidationError("The year must be a valid number.")
        return year
    def clean(self):
        cleaned_data = super().clean()
        # Validate if all rates are non-negative
        for field_name in ['validity_year', 'avs_item', 'ac_item', 'ac2_item', 'laap_item',
                  'laanp_item', 'laac_item', 'laace_item',
                  'amat_item', 'alfa_item', 'apgmal_item', 'alpetiteenfance_item',
                  'child_alloc_1_item', 'child_alloc_2_item']:
                  value = cleaned_data.get(field_name)
                  if value is not None and value < 0:
                    self.add_error(field_name, "The rate cannot be negative.")
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ModifyYearForm(forms.ModelForm):
    class Meta:
        model = salary_items
        fields = ['validity_year', 'avs_item', 'ac_item', 'ac2_item', 'laap_item',
                  'laanp_item', 'laac_item', 'laace_item',
                  'amat_item', 'alfa_item', 'apgmal_item', 'alpetiteenfance_item',
                  'child_alloc_1_item', 'child_alloc_2_item']



class OverviewForm(forms.Form):
    year = forms.CharField()
    month = forms.CharField()
    employee = forms.CharField()
