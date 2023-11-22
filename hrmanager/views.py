from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Employees, salary_items, GeneratorData
from django.views import View
from django.urls import reverse_lazy
from .forms import NewEmployeeForm, ModifyEmployeeForm, NewYearForm, ModifyYearForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class EmployeesList(generic.ListView):
    model = Employees
    queryset = Employees.objects.filter(
        employees_status=0).order_by('last_name')
    template_name = 'employee_list.html'
    paginate_by = 6


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
        print("NewEmployeeForm is valid!")
        return response

    def form_invalid(self, form):
        print("NewEmployeeForm is invalid!")
        print(form.errors)
        return super().form_invalid(form)


class ModifyEmployeeView(generic.edit.UpdateView):
    model = Employees
    form_class = ModifyEmployeeForm
    template_name = 'employee_modify.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        print("ModifyEmployeeForm is valid!")
        return redirect('Detailofemployees', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        print("ModifyEmployeeForm is invalid!")
        print(form.errors)
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Employees, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_pk'] = self.object.pk
        context['form'] = ModifyEmployeeForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('Detailofemployees', kwargs={'pk': self.kwargs['pk']})


class YearList(generic.ListView):
    model = salary_items
    queryset = salary_items.objects.order_by('validity_year')
    template_name = 'year_list.html'
    paginate_by = 6


class YearDetailView(generic.DetailView):
    model = salary_items
    template_name = 'year_detail.html'
    context_object_name = 'selected_year'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_year_pk'] = self.object.pk
        return context


class YearAddView(generic.edit.CreateView):
    model = salary_items
    template_name = 'year_add.html'
    form_class = NewYearForm
    success_url = reverse_lazy('Yearview')

    def form_valid(self, form):
        response = super().form_valid(form)
        print("NewItemForm is valid!")
        return response

    def form_invalid(self, form):
        print("NewItemForm is invalid!")
        print(form.errors)
        return super().form_invalid(form)


class ModifyYearView(generic.edit.UpdateView):
    model = salary_items
    form_class = ModifyYearForm
    template_name = 'year_modify.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        print("AddYearForm is valid!")
        return redirect('Detailofyears', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        print("AddYearForm is invalid!")
        print(form.errors)
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(salary_items, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_pk'] = self.object.pk
        context['form'] = ModifyYearForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('Detailofyears', kwargs={'pk': self.kwargs['pk']})


class GeneratorYearView(View):
    template_name = 'generator_year.html'

    def get(self, request, *args, **kwargs):
        years = set(salary_items.objects.values_list(
            'validity_year', flat=True))
        return render(request, self.template_name, {'years': years})


class GeneratorMonthView(View):
    template_name = 'generator_month.html'

    def get(self, request, year, *args, **kwargs):
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return render(request, self.template_name, {'year': year, 'months': months})


class GeneratorMonthlyTableView(View):
    template_name = 'generator_monthly_table.html'

    def get(self, request, year, month, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
