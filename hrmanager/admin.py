from django.contrib import admin
from .models import Employees
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

# admin.site.register(Employees)
