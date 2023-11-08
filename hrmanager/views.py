from django.shortcuts import render
from django.views import generic
from .models import Employees
from django.views import View
#from django import template

#register = template.Library()


#@register.filter
#def get_model_fields(model):
#    return model._meta.fields

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
    # context_object_name = 'employees'


class EnployeeDetailView(generic.DetailView):
    model = Employees
    template_name = 'employee_detail.html'
    context_object_name = 'selected_employee'
