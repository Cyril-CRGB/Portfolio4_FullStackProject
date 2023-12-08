# Importing necessary modules and classes
from django.contrib import admin
from .models import Employees, salary_items, GeneratorData
from django_summernote.admin import SummernoteModelAdmin


# Registering the Employees model with the admin site
@admin.register(Employees)
class EmployeesAdmin(SummernoteModelAdmin):
    # Prepopulating the 'title' field based on 'last_name' and 'first_name'
    prepopulated_fields = {'title': ('last_name', 'first_name')}
    # Adding filters for the list view in the admin site
    list_filter = ('employees_status', 'start_date')
    # Displaying specific fields in the list view
    list_display = ('last_name', 'first_name',
                    'start_date', 'employees_status')
    # Adding a search functionality for specific fields
    search_fields = ['last_name', 'first_name']
    # Defining custom actions for bulk updates
    actions = ['deactivate_employee', 'activate_employee']

    # Custom action to deactivate selected employees
    def deactivate_employee(self, request, queryset):
        queryset.update(employees_status=1)

    # Custom action to activate selected employees
    def activate_employee(self, request, queryset):
        queryset.update(employees_status=0)


# Registering the salary_items model with the admin site
@admin.register(salary_items)
class YearAdmin(SummernoteModelAdmin):
    # Adding a search functionality for the 'validity_year' field
    search_fields = ['validity_year']


# Registering the GeneratorData model with the admin site
@admin.register(GeneratorData)
class DataAdmin(SummernoteModelAdmin):
    # Adding a search functionality for the 'validity_year' field
    search_fields = ['validity_year']
    # Adding filters for the list view in the admin site
    list_filter = ('gd_year', 'gd_month')
    # Displaying specific fields in the list view
    list_display = ('gd_year', 'gd_month',
                    'gd_monthly_table_saved', 'gd_monthly_table_paid')
    # Adding a search functionality for specific fields
    search_fields = ['last_name', 'first_name']
