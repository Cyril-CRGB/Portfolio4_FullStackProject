from django.contrib import admin
from .models import Employees
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Employees)
class EmployeesAdmin(SummernoteModelAdmin):
    # summernote_fields = ('content')
    # prepopulated_fields = {'fieldsname': ('referredtofieldname',)}
    list_filter = ('employees_status', 'start_date')

# admin.site.register(Employees)
