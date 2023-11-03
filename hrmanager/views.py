from django.shortcuts import render
from django.views import generic
from .models import Employees


class EmployeesList(generic.ListView):
    model = Employees
    queryset = Employees.objects.filter(
        employees_status=0).order_by('-last_name')
    template_name = 'index.html'
    paginate_by = 6
