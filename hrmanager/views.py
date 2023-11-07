from django.shortcuts import render
from django.views import generic
from .models import Employees
from django.views import View


# def HomeView(request):
#    return render(request, 'index.html')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class EmployeesList(generic.ListView):
    model = Employees
    queryset = Employees.objects.filter(
        employees_status=0).order_by('last_name')
    template_name = 'employee_list.html'
    paginate_by = 6

class EmployeesDetail(generic.ListView):
    model = Employees
    queryset = Employees.objects.all()
    template_name = 'employee_detail.html'
