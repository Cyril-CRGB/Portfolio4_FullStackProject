from django.shortcuts import render
from django.views import generic
from .models import Employees
from django.views import View
from django.urls import reverse_lazy
# from django import template

# register = template.Library()


# @register.filter
# def get_model_fields(model):
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


class EnployeeAddView(generic.edit.CreateView):
    model = Employees
    template_name = 'employee_add.html'
    fields = ['first_name', 'last_name', 'employees_gender',
              'employees_marital_status', 'children_for_allocations_type_1', 'children_for_allocations_type_2',
              'birth_date', 'employees_age', 'email_adress', 'phone_number', 'emergency_contact', 'emergency_phonenumber',
              'employee_picture', 'social_security_number', 'employees_bankaccount', 'start_date', 'end_date',
              'employees_holiday_rights', 'base_monthly_salary', 'employees_phone_allocation',
              'employees_representation_allocation', 'seniority', 'employees_status']
    success_url = reverse_lazy('Listofemployees')
