from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Employees
from django.views import View
from django.urls import reverse_lazy
from .forms import NewEmployeeForm, ModifyEmployeeForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_employee_pk'] = self.object.pk
        return context


class EnployeeAddView(generic.edit.CreateView):
    model = Employees
    template_name = 'employee_add.html'
    form_class = NewEmployeeForm
    success_url = reverse_lazy('Listofemployees')

    def form_valid(self, form):
        response = super().form_valid(form)
        print("Form EnployeeAddView is valid!")
        return response

    def form_invalid(self, form):
        print("Form EnployeeAddView is invalid!")
        print(form.errors)
        return super().form_invalid(form)


class ModifyEmployeeView(generic.edit.UpdateView):
    model = Employees
    form_class = ModifyEmployeeForm
    template_name = 'employee_modify.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        print("Form ModifyEmployeeView is valid!")
        return redirect('Detailofemployees', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        print("Form ModifyEmployeeView is invalid!")
        print(form.errors)
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Employees, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_pk'] = self.object.pk
        return context

    def get_success_url(self):
        return reverse_lazy('Detailofemployees', kwargs={'pk': self.kwargs['pk']})
