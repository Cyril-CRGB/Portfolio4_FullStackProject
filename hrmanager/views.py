from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Employees, salary_items, GeneratorData
from django.views import View
from django.urls import reverse_lazy, reverse
from .forms import NewEmployeeForm, ModifyEmployeeForm, NewYearForm, ModifyYearForm, GeneratorYearForm
from django.http import HttpResponseRedirect


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
    form_class = GeneratorYearForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['selected_year']
            salary_item = get_object_or_404(
                salary_items, validity_year=selected_year)
            return HttpResponseRedirect(reverse('generator_month', args=[selected_year]))
        else:
            print("GeneratorYearForm is invalid!")
            print(form.errors)
            return render(request, self.template_name, {'form': form})
    # def get(self, request, *args, **kwargs):
    #    years = set(salary_items.objects.values_list(
    #        'validity_year', flat=True))
    #    return render(request, self.template_name, {'years': years})


class GeneratorMonthView(View):
    template_name = 'generator_month.html'

    def get(self, request, year, *args, **kwargs):
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        context = {'year': year, 'months': months, 'selected_year': year}
        return render(request, self.template_name, context)


class GeneratorMonthlyTableView(View):
    model = GeneratorData
    template_name = 'generator_monthly_table.html'

    def get(self, request, year, month, *args, **kwargs):
        # generator_data, created = GeneratorData.objects.get_or_create(
        #    gd_year=year, gd_month=month)
        generator_data_instance = get_object_or_404(
            GeneratorData, gd_year=year, gd_month=month)
        salary_item = get_object_or_404(salary_items, validity_year=year)
        generator_data_instance.gd_avs_item = -salary_item.avs_item
        generator_data_instance.save()
        # 'generator_data': generator_data,
        context = {'generator_data_instance': generator_data_instance, }
        return render(request, self.template_name, context)
