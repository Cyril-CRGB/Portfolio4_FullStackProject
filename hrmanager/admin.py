from django.contrib import admin
from .models import Employees, salary_items, GeneratorData
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Employees)
class EmployeesAdmin(SummernoteModelAdmin):
    # summernote_fields = ('content')

    prepopulated_fields = {'title': ('last_name', 'first_name')}
    # readonly_fields = ('title', )
    list_filter = ('employees_status', 'start_date')
    list_display = ('last_name', 'first_name',
                    'start_date', 'employees_status')
    search_fields = ['last_name', 'first_name']
    actions = ['deactivate_employee', 'activate_employee']

    def deactivate_employee(self, request, queryset):
        queryset.update(employees_status=1)

    def activate_employee(self, request, queryset):
        queryset.update(employees_status=0)


# admin.site.register(Employees)


@admin.register(salary_items)
class YearAdmin(SummernoteModelAdmin):
    search_fields = ['validity_year']


@admin.register(GeneratorData)
class DataAdmin(SummernoteModelAdmin):
    search_fields = ['validity_year']
    list_filter = ('gd_year', 'gd_month')
    list_display = ('gd_year', 'gd_month',
                    'gd_monthly_table_saved', 'gd_monthly_table_paid')
    search_fields = ['last_name', 'first_name']
