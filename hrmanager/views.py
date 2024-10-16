# Importing the necessary modules or classes
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Employees, salary_items, GeneratorData
from django.urls import reverse_lazy, reverse
from .forms import NewEmployeeForm, ModifyEmployeeForm, NewYearForm, ModifyYearForm, OverviewForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from calendar import month_name, monthrange
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.utils.safestring import mark_safe
from django.views.generic.edit import DeleteView


# Defining a class named HomeView that inherits from the View class
class HomeView(View):
    # Handling HTTP GET requests
    def get(self, request, *args, **kwargs):
        # Rendering the 'index.html' template and returning the result
        return render(request, 'index.html')

# A view to list all active employees
class EmployeesList(generic.ListView):
    # Specify the model to be used for this view
    model = Employees
    # Defin a custom queryset, filtering employees with status 0 and ordering by last name
    #queryset = Employees.objects.filter(
    #    employees_status=0).order_by('last_name')
    # Set the template name to be used for rendering this view
    # Override get_queryset to get all empoyees, ordered by last name
    def get_queryset(self):
        return Employees.objects.order_by('last_name')
    template_name = 'employee_list.html'
    # Specify the number of items to display per page, enabling pagination
    paginate_by = 6

# A view to display details of an employee
class EnployeeDetailView(generic.DetailView):
    # Speciy the model to be used for this view
    model = Employees
    # Set the template name to be used for rendering this view
    template_name = 'employee_detail.html'
    # Define the name to be used for the context variable in the template
    context_object_name = 'selected_employee'

    # Override the get_context_data method to add additional context data
    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context
        context = super().get_context_data(**kwargs)
        # Add the primary key of the selected employee to the context
        context['selected_employee_pk'] = self.object.pk
        # Return the update context
        return context

# A view to add a new employee
class EnployeeAddView(generic.edit.CreateView):
    # Specify the model to be used for this view
    model = Employees
    # Set the template name to be used for rendering this view
    template_name = 'employee_add.html'
    # Specify the form class to be used for adding a new employee
    form_class = NewEmployeeForm
    # Set the URL to redirect to after a successful addition of a new employee
    success_url = reverse_lazy('Listofemployees')
    # Check if the form is invalide before saving
    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the employee. Please correct the highlighted fields.')
        return super().form_invalid(form)
    # Check if the form is valide before saving
    def form_valid(self, form):
        messages.success(self.request, 'Employee added successfully.')
        return super().form_valid(form)

# A view to modify an existing employee
class ModifyEmployeeView(generic.edit.UpdateView):
    # Specify the model to be used for this view
    model = Employees
    # Specify the form class to be used for updating employee information
    form_class = ModifyEmployeeForm
    # Set the template name to be used for rendering this view
    template_name = 'employee_modify.html'

    # Override the get_object method to retrieve the employee object to be updated
    def get_object(self, queryset=None):
        # Retrieve the primary key from the URL parameters
        pk = self.kwargs.get('pk')
        # Get the employee object or return a 404 response if not found
        return get_object_or_404(Employees, pk=pk)

    # Override the get_context_data method to add additional context data
    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context
        context = super().get_context_data(**kwargs)
        # Add the current primary key and the form for the current employee to the context
        context['current_pk'] = self.object.pk
        context['form'] = ModifyEmployeeForm(instance=self.object)
        # Return the updated context
        return context

    # Override the get_succes_url method to define the URL to redirect to after a successful update
    def get_success_url(self):
        # Return the URL for displaying the details of the updated employee
        return reverse_lazy('Detailofemployees', kwargs={'pk': self.kwargs['pk']})

    # Check if the form is invalide before saving
    def form_invalid(self, form):
        # Extract and format the error messages without HTML
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field.replace('_', ' ').capitalize()}: {error}")
        # Combine all error messages into one string
        error_message_str = "<br>".join(error_messages)
        # Display the error message in the user interface
        messages.error(self.request, mark_safe(f"Please correct the following fields:<br>{error_message_str}"))
        return self.render_to_response(self.get_context_data(form=form))

    # Check if the form is valide before saving
    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully.')
        return super().form_valid(form)



# A view to list all available salary years
class YearList(generic.ListView):
    # Specify the model to be used for this view
    model = salary_items
    # Define a custom queryset, ordering salary items by validity year
    queryset = salary_items.objects.order_by('validity_year')
    # Set the template name to be used for rendering this view
    template_name = 'year_list.html'
    # Specify the number of items to display per page, enabling pagination
    paginate_by = 6

# A view to display details of a salary year
class YearDetailView(generic.DetailView):
    # Specifying the model to be used by the view
    model = salary_items
    # Specifying the template to be rendered
    template_name = 'year_detail.html'
    # Specifying the context variable name to use in the template
    context_object_name = 'selected_year'

    # Overriding the get_context_data method to provide additional context data
    def get_context_data(self, **kwargs):
        # Calling the get_context_data method of the superclass
        context = super().get_context_data(**kwargs)
        # Adding a custom context variable 'selected_year_pk' with the primary key of the object
        context['selected_year_pk'] = self.object.pk
        # Returning the updated context
        return context

# A view to add a new salary year
class YearAddView(generic.edit.CreateView):
    # Specify the model to be used for this view
    model = salary_items
    # Set the template name to be used for rendering this view
    template_name = 'year_add.html'
    # Specify the form class to be used for adding a new salary year
    form_class = NewYearForm
    # Set the URL to redirect to after a successful addition of a new salary year
    success_url = reverse_lazy('Yearview')
    # Check if the form is invalide before saving
    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the year. Please correct the highlighted fields.')
        return super().form_invalid(form)
    # Check if the form is valide before saving
    def form_valid(self, form):
        messages.success(self.request, 'Year added successfully.')
        return super().form_valid(form)

# A view to modify an existing salary year
class ModifyYearView(generic.edit.UpdateView):
    # Specify the model to be used for this view
    model = salary_items
    # Specify the form class to be used for updating salary year information
    form_class = ModifyYearForm
    # Set the template name to be used for rendering this view
    template_name = 'year_modify.html'

    # Override the get_object method to retrieve the salary year object to be updated
    def get_object(self, queryset=None):
        # Retrieve the primary key from the URL parameters
        pk = self.kwargs.get('pk')
        # Get the salary year object or return a 404 response if not found
        return get_object_or_404(salary_items, pk=pk)

    # Override the get_context_data method to add additional context data
    def get_context_data(self, **kwargs):
        # Call the superclass method to get the default context
        context = super().get_context_data(**kwargs)
        # Add the current primary key and the form for the current salary year to the context
        context['current_pk'] = self.object.pk
        context['form'] = ModifyYearForm(instance=self.object)
        # Return the updated context
        return context

    # Override the get_success_url method to define the URL to redirect to after a successful update
    def get_success_url(self):
        # Return the URL for displaying the details of the updated salary year
        return reverse_lazy('Detailofyears', kwargs={'pk': self.kwargs['pk']})

        # Check if the form is invalide before saving
    def form_invalid(self, form):
        # Extract and format the error messages without HTML
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field.replace('_', ' ').capitalize()}: {error}")
        # Combine all error messages into one string
        error_message_str = "<br>".join(error_messages)
        # Display the error message in the user interface
        messages.error(self.request, mark_safe(f"Please correct the following fields:<br>{error_message_str}"))
        return self.render_to_response(self.get_context_data(form=form))

    # Check if the form is valide before saving
    def form_valid(self, form):
        messages.success(self.request, 'Year updated successfully.')
        return super().form_valid(form)


class GeneratorYearView(View):
    template_name = 'generator_year.html'

    def get(self, request, *args, **kwargs):
        # Retrieve all unique validity years from the SalaryItems model
        validity_years = salary_items.objects.values_list(
            'validity_year', flat=True).distinct()
        # List to store year statuses
        year_statuses = []

        # Set default values for variables that will be used in the loop
        is_previous_year_completed = 0
        is_current_year_completed = 0

        # Find the minimum year
        min_year = min(validity_years, default=None)

        # Display message if no previous year exists
        if not validity_years:
            messages.warning(request, "Please create a new year first.")
            context = {
                'validity_years': validity_years,
                'year_statuses': year_statuses,
                'is_previous_year_completed': is_previous_year_completed,
                'is_current_year_completed': is_current_year_completed
            }
            return render(request, self.template_name, context)

        for year in validity_years:
            # Check if the previous year is completed and not None
            previous_year = int(year) - 1
            is_previous_year_completed = GeneratorData.objects.filter(
                gd_year=previous_year, gd_month=12, gd_monthly_table_paid__isnull=False).distinct().count()
            # Check if the current year is completed
            is_current_year_completed = GeneratorData.objects.filter(
                gd_year=year, gd_month=12, gd_monthly_table_paid__isnull=False).distinct().count()

            if is_current_year_completed != 0:
                status = "Completed"
            elif is_previous_year_completed != 0 and is_current_year_completed == 0:
                status = "Current"
            elif year == min_year:
                # If it's the minimum year, set status to 'Current'
                status = "Current"
            else:
                # If previous year is not completed, set status to not available
                status = "not_available"

            # Append year and status to the list
            year_statuses.append(
                (year, status, is_previous_year_completed, is_current_year_completed))

        # Pass the validity years to the template
        context = {'validity_years': validity_years, 'year_statuses': year_statuses,
                   'is_previous_year_completed': is_previous_year_completed, 'is_current_year_completed': is_current_year_completed}
        return render(request, self.template_name, context)


class GeneratorMonthView(View):
    template_name = 'generator_month.html'

    def get(self, request, year, *args, **kwargs):

        months = [
            'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ]

        generator_check_data_exist = {
            month_num: GeneratorData.objects.filter(
                gd_year=year, gd_month=month_num).exists()
            for month_num, month in enumerate(range(1, 13), start=1)
        }

        generator_check_is_paid = {
            month_num: GeneratorData.objects.filter(
                gd_year=year, gd_month=month_num, gd_monthly_table_paid__isnull=False).exists()
            for month_num, month in enumerate(range(1, 13), start=1)
        }

        generator_check_combined = {
            month_num: {
                'has_data': generator_check_data_exist[month_num],
                'is_paid': generator_check_is_paid[month_num],
                'has_data_truebefore_falseafter': (
                    not generator_check_data_exist[month_num]
                    and generator_check_data_exist.get(month_num - 1, True)
                    and not generator_check_data_exist.get(month_num + 1, False)
                ),
                'is_paid_truebefore_falseafter': (
                    not generator_check_is_paid[month_num]
                    and generator_check_is_paid.get(month_num - 1, True)
                    and not generator_check_is_paid.get(month_num + 1, False)
                ),
            }
            for month_num, month in enumerate(range(1, 13), start=1)
        }

        context = {'year': year, 'months': months,
                   'generator_check_combined': generator_check_combined}
        return render(request, self.template_name, context)


class GeneratorEmployeesView(View):
    template_name = 'generator_employees.html'

    def get(self, request, year, month, *args, **kwargs):
        # find all employees with status 0 (active)
        employees = Employees.objects.filter(
            employees_status=0
        ).values('first_name', 'last_name', 'social_security_number')

        context = {'year': year, 'month': month, 'employees': employees}
        return render(request, self.template_name, context)


class GeneratorMonthlyTableView(View):
    template_name = 'generator_monthly_table.html'

    def get(self, request, year, month, *args, **kwargs):
        first_day = datetime(year, month, 1).date()
        last_day = datetime(year, month, monthrange(year, month)[1]).date()
        employees = Employees.objects.filter(employees_status=0).values(
            'first_name', 'last_name', 'social_security_number', 'base_monthly_salary', 'start_date', 'end_date',
            'children_for_allocations_type_1', 'children_for_allocations_type_2', 'public_transportation_fees',
            'extraordinary_salary', 'LPP_deduction_employee', 'employees_phone_allocation', 'employees_representation_allocation',
            'expense_report')

        for employee in employees:
            start_date = employee['start_date']
            end_date = employee['end_date']
            # calculating worked days based on the conditions
            if start_date > last_day or (end_date and end_date < first_day):
                # dealing with exceptions
                worked_days = 0
            elif start_date > first_day:
                worked_days = (last_day - start_date).days + 1
            elif end_date and end_date < last_day:
                worked_days = (end_date - first_day).days + 1
            else:
                worked_days = (last_day - first_day).days + 1

            base_monthly_salary = employee['base_monthly_salary']
            calculated_monthly_salary = Decimal(
                base_monthly_salary) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
            children_alloc_type_1_str = employee['children_for_allocations_type_1']
            children_alloc_type_1 = int(
                children_alloc_type_1_str) if children_alloc_type_1_str.isdigit() else 0
            children_allowance_type_1 = Decimal(
                children_alloc_type_1 * 311) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
            children_alloc_type_2_str = employee['children_for_allocations_type_2']
            children_alloc_type_2 = int(
                children_alloc_type_2_str) if children_alloc_type_2_str.isdigit() else 0
            children_allowance_type_2 = Decimal(
                children_alloc_type_2 * 411) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
            public_transportation_fees = employee['public_transportation_fees']
            extraordinary_salary = employee['extraordinary_salary']
            salary_for_social_deduction = round(float(
                calculated_monthly_salary + public_transportation_fees + extraordinary_salary), 2)
            salary_for_taxes = round(float(calculated_monthly_salary + public_transportation_fees +
                                     extraordinary_salary + int(children_alloc_type_1) * 311 + int(children_alloc_type_2) * 411), 2)
            avs_item = salary_items.objects.get(validity_year=year).avs_item
            calculated_avs_employee = round(
                float(avs_item), 2) * salary_for_social_deduction * -1 / 100
            ac_item = salary_items.objects.get(validity_year=year).ac_item
            calculated_ac_employee = round(
                float(ac_item), 2) * salary_for_social_deduction * -1 / 100
            ac2_item = salary_items.objects.get(validity_year=year).ac2_item
            calculated_ac2_employee = round(
                float(ac2_item), 2) * salary_for_social_deduction * -1 / 100
            laanp_item = salary_items.objects.get(
                validity_year=year).laanp_item
            calculated_laanp_employee = round(
                float(laanp_item), 2) * salary_for_social_deduction * -1 / 100
            amat_item = salary_items.objects.get(
                validity_year=year).amat_item
            calculated_amat_employee = round(
                float(amat_item), 2) * salary_for_social_deduction * -1 / 100
            apgmal_item = salary_items.objects.get(
                validity_year=year).apgmal_item
            calculated_apgmal_employee = round(
                float(apgmal_item), 2) * salary_for_social_deduction * -1 / 100
            LPP_deduction_employee = employee['LPP_deduction_employee']
            calculated_total_deduction_employee = round(float(calculated_apgmal_employee), 2) + round(float(calculated_amat_employee), 2) + round(float(
                calculated_laanp_employee), 2) + round(float(calculated_ac2_employee), 2) + round(float(calculated_ac_employee), 2) + round(float(calculated_avs_employee), 2) + round(float(LPP_deduction_employee), 2)
            employees_phone_allocation = employee['employees_phone_allocation']
            employees_representation_allocation = employee['employees_representation_allocation']
            expense_report = employee['expense_report']
            calculated_correction_non_financial_wage = public_transportation_fees * -1
            calculated_paid_salary = round(float(salary_for_social_deduction), 2) + round(float(calculated_total_deduction_employee), 2) + round(float(employees_phone_allocation), 2) + round(
                float(employees_representation_allocation), 2) + round(float(expense_report), 2) + round(float(calculated_correction_non_financial_wage), 2)

            employee['worked_days'] = worked_days
            employee['calculated_monthly_salary'] = round(
                float(calculated_monthly_salary), 2)
            employee['calculated_child_allocation_1'] = round(
                float(children_allowance_type_1), 2)
            employee['calculated_child_allocation_2'] = round(
                float(children_allowance_type_2), 2)
            employee['salary_for_social_deduction'] = salary_for_social_deduction
            employee['salary_for_taxes'] = salary_for_taxes
            employee['calculated_avs_employee'] = round(
                float(calculated_avs_employee), 2)
            employee['calculated_ac_employee'] = round(
                float(calculated_ac_employee), 2)
            employee['calculated_ac2_employee'] = round(
                float(calculated_ac2_employee), 2)
            employee['calculated_laanp_employee'] = round(
                float(calculated_laanp_employee), 2)
            employee['calculated_amat_employee'] = round(
                float(calculated_amat_employee), 2)
            employee['calculated_apgmal_employee'] = round(
                float(calculated_apgmal_employee), 2)
            employee['calculated_total_deduction_employee'] = round(
                float(calculated_total_deduction_employee), 2)
            employee['calculated_correction_non_financial_wage'] = calculated_correction_non_financial_wage
            employee['calculated_paid_salary'] = round(
                float(calculated_paid_salary), 2)

        context = {'year': year, 'month': month, 'employees': employees}
        return render(request, self.template_name, context)


class GeneratorSaveMonthlyTableView(View):

    def get(self, request, year, month, *args, **kwargs):
        first_day = datetime(year, int(month), 1).date()
        last_day = datetime(
            year, int(month), monthrange(year, int(month))[1]).date()
        employees = Employees.objects.filter(employees_status=0).values(
            'title', 'first_name', 'last_name', 'social_security_number', 'base_monthly_salary', 'start_date', 'end_date',
            'children_for_allocations_type_1', 'children_for_allocations_type_2', 'public_transportation_fees',
            'extraordinary_salary', 'LPP_deduction_employee', 'employees_phone_allocation', 'employees_representation_allocation',
            'expense_report')

        existing_data = GeneratorData.objects.filter(
            gd_year=str(year), gd_month=str(month)).first()

        if existing_data:
            return render(request, 'generator_monthly_table.html', {'existing_data': True, 'year': year, 'month': month})
            # alert_html = render_to_string('alert_existing_data.html')
            # return HttpResponse(alert_html)

        else:

            for employee in employees:
                start_date = employee['start_date']
                end_date = employee['end_date']
                # calculating worked days based on the conditions
                if start_date > last_day or (end_date and end_date < first_day):
                    # dealing with exceptions
                    worked_days = 0
                elif start_date > first_day:
                    worked_days = (last_day - start_date).days + 1
                elif end_date and end_date < last_day:
                    worked_days = (end_date - first_day).days + 1
                else:
                    worked_days = (last_day - first_day).days + 1

                base_monthly_salary = employee['base_monthly_salary']
                calculated_monthly_salary = Decimal(
                    base_monthly_salary) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
                children_alloc_type_1_str = employee['children_for_allocations_type_1']
                children_alloc_type_1 = int(
                    children_alloc_type_1_str) if children_alloc_type_1_str.isdigit() else 0
                children_allowance_type_1 = Decimal(
                    children_alloc_type_1 * 311) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
                children_alloc_type_2_str = employee['children_for_allocations_type_2']
                children_alloc_type_2 = int(
                    children_alloc_type_2_str) if children_alloc_type_2_str.isdigit() else 0
                children_allowance_type_2 = Decimal(
                    children_alloc_type_2 * 411) / Decimal((last_day - first_day).days + 1) * Decimal(worked_days)
                public_transportation_fees = employee['public_transportation_fees']
                extraordinary_salary = employee['extraordinary_salary']
                salary_for_social_deduction = round(float(
                    calculated_monthly_salary + public_transportation_fees + extraordinary_salary), 2)
                salary_for_taxes = round(float(calculated_monthly_salary + public_transportation_fees +
                                               extraordinary_salary + int(children_alloc_type_1) * 311 + int(children_alloc_type_2) * 411), 2)
                avs_item = salary_items.objects.get(
                    validity_year=year).avs_item
                calculated_avs_employee = round(
                    float(avs_item), 2) * salary_for_social_deduction * -1 / 100
                ac_item = salary_items.objects.get(validity_year=year).ac_item
                calculated_ac_employee = round(
                    float(ac_item), 2) * salary_for_social_deduction * -1 / 100
                ac2_item = salary_items.objects.get(
                    validity_year=year).ac2_item
                calculated_ac2_employee = round(
                    float(ac2_item), 2) * salary_for_social_deduction * -1 / 100
                laanp_item = salary_items.objects.get(
                    validity_year=year).laanp_item
                calculated_laanp_employee = round(
                    float(laanp_item), 2) * salary_for_social_deduction * -1 / 100
                amat_item = salary_items.objects.get(
                    validity_year=year).amat_item
                calculated_amat_employee = round(
                    float(amat_item), 2) * salary_for_social_deduction * -1 / 100
                apgmal_item = salary_items.objects.get(
                    validity_year=year).apgmal_item
                calculated_apgmal_employee = round(
                    float(apgmal_item), 2) * salary_for_social_deduction * -1 / 100
                LPP_deduction_employee = employee['LPP_deduction_employee']
                calculated_total_deduction_employee = round(float(calculated_apgmal_employee), 2) + round(float(calculated_amat_employee), 2) + round(float(
                    calculated_laanp_employee), 2) + round(float(calculated_ac2_employee), 2) + round(float(calculated_ac_employee), 2) + round(float(calculated_avs_employee), 2) + round(float(LPP_deduction_employee), 2)
                employees_phone_allocation = employee['employees_phone_allocation']
                employees_representation_allocation = employee['employees_representation_allocation']
                expense_report = employee['expense_report']
                calculated_correction_non_financial_wage = public_transportation_fees * -1
                calculated_paid_salary = round(float(salary_for_social_deduction), 2) + round(float(calculated_total_deduction_employee), 2) + round(float(employees_phone_allocation), 2) + round(
                    float(employees_representation_allocation), 2) + round(float(expense_report), 2) + round(float(calculated_correction_non_financial_wage), 2)

                employee['worked_days'] = worked_days
                employee['calculated_monthly_salary'] = round(
                    float(calculated_monthly_salary), 2)
                employee['calculated_child_allocation_1'] = round(
                    float(children_allowance_type_1), 2)
                employee['calculated_child_allocation_2'] = round(
                    float(children_allowance_type_2), 2)
                employee['salary_for_social_deduction'] = salary_for_social_deduction
                employee['salary_for_taxes'] = salary_for_taxes
                employee['calculated_avs_employee'] = round(
                    float(calculated_avs_employee), 2)
                employee['calculated_ac_employee'] = round(
                    float(calculated_ac_employee), 2)
                employee['calculated_ac2_employee'] = round(
                    float(calculated_ac2_employee), 2)
                employee['calculated_laanp_employee'] = round(
                    float(calculated_laanp_employee), 2)
                employee['calculated_amat_employee'] = round(
                    float(calculated_amat_employee), 2)
                employee['calculated_apgmal_employee'] = round(
                    float(calculated_apgmal_employee), 2)
                employee['calculated_total_deduction_employee'] = round(
                    float(calculated_total_deduction_employee), 2)
                employee['calculated_correction_non_financial_wage'] = calculated_correction_non_financial_wage
                employee['calculated_paid_salary'] = round(
                    float(calculated_paid_salary), 2)

                generator_data = GeneratorData.objects.create(
                    gd_year=year,
                    gd_month=month,  # assuming month is a string, adjust if necessary
                    gd_title=employee['title'],
                    gd_first_name=employee['first_name'],
                    gd_last_name=employee['last_name'],
                    gd_start_date=start_date,
                    gd_end_date=end_date,
                    gd_first_day_of_the_month_date=first_day,
                    gd_last_day_of_the_month_date=last_day,
                    gd_worked_days=worked_days,
                    gd_base_monthly_salary=employee['base_monthly_salary'],
                    gd_monthly_salary=calculated_monthly_salary,
                    gd_child_allocation_1=children_allowance_type_1,
                    gd_child_allocation_2=children_allowance_type_2,
                    gd_total_monthly_wage=salary_for_social_deduction,  # Watch out
                    gd_total_monthly_wage_for_social_insurance=salary_for_social_deduction,
                    gd_total_monthly_wage_for_social_taxes=salary_for_taxes,
                    gd_avs_item=calculated_avs_employee,
                    gd_ac_item=calculated_ac_employee,
                    gd_ac2_item=calculated_ac2_employee,
                    gd_laanp_item=calculated_laanp_employee,
                    gd_amat_item=calculated_amat_employee,
                    gd_apgmal_item=calculated_apgmal_employee,
                    gd_employees_phone_allocation=employees_phone_allocation,
                    gd_employees_representation_allocation=employees_representation_allocation,
                    gd_expense_report=expense_report,
                    gd_public_transportation_fees=public_transportation_fees,
                    gd_paid_salary=calculated_paid_salary,
                    gd_extraordinary_salary=extraordinary_salary,
                    gd_LPP_deduction_employee=LPP_deduction_employee,
                    gd_total_deduction_employee=calculated_total_deduction_employee,
                    gd_correction_non_financial_wage=calculated_correction_non_financial_wage
                )

            message = "Data has been created and saved successfully!"
            messages.success(request, message)

            return redirect('generator_month', year=year)


class GeneratorDeleteMonthlyDataView(View):

    def post(self, request, year, month, *args, **kwargs):
        # Check if there is data to delete
        data_to_delete = GeneratorData.objects.filter(
            gd_year=year, gd_month=month)

        if data_to_delete.exists():
            # Data found and deleted
            data_to_delete.delete()
            message = "Data has been deleted successfully."
            messages.success(request, message)
        else:
            # No data found
            message = "No data found. Please save the data first."
            messages.warning(request, message)

        return redirect('generator_month', year=year)


class GeneratorSeeView(View):
    template_name = 'generator_see.html'

    def get(self, request, year, month, *args, **kwargs):

        # Check if data exists
        generator_data = GeneratorData.objects.filter(
            gd_year=year, gd_month=month)

        if not generator_data.exists():
            # No data found, redirect with a warning message
            message = "No data to visualize. Please save it first."
            messages.warning(request, message)
            return redirect('generator_month', year=year)
        else:
            # Data exist, proceed with rendering the template
            generator_data = GeneratorData.objects.filter(
                gd_year=year, gd_month=month).values(
                'gd_year', 'gd_month', 'gd_title', 'gd_first_name', 'gd_last_name', 'gd_start_date', 'gd_end_date',
                'gd_first_day_of_the_month_date', 'gd_last_day_of_the_month_date', 'gd_worked_days',
                'gd_base_monthly_salary', 'gd_monthly_salary', 'gd_child_allocation_1', 'gd_child_allocation_2',
                'gd_total_monthly_wage', 'gd_total_monthly_wage_for_social_insurance', 'gd_total_monthly_wage_for_social_taxes',
                'gd_avs_item', 'gd_ac_item', 'gd_ac2_item', 'gd_laap_item', 'gd_laanp_item', 'gd_laac_item',
                'gd_laace_item', 'gd_amat_item', 'gd_alfa_item', 'gd_apgmal_item', 'gd_alpetiteenfance_item',
                'gd_total_social_deduction', 'gd_employees_phone_allocation', 'gd_employees_representation_allocation',
                'gd_expense_report', 'gd_public_transportation_fees', 'gd_paid_salary', 'gd_monthly_table_saved',
                'gd_monthly_table_paid', 'gd_extraordinary_salary', 'gd_LPP_deduction_employee', 'gd_total_deduction_employee',
                'gd_correction_non_financial_wage')

        context = {'generator_data': generator_data}
        return render(request, self.template_name, context)


class GeneratorPayView(View):
    def post(self, request, year, month, *args, **kwargs):
        generator_data_list = GeneratorData.objects.filter(
            gd_year=year, gd_month=month)

        if generator_data_list.exists():
            if not any(generator_data.gd_monthly_table_paid for generator_data in generator_data_list):
                for generator_data in generator_data_list:
                    generator_data.gd_monthly_table_paid = timezone.now()
                    generator_data.save()
                messages.success(request, 'Payment successful.')
            else:
                messages.warning(
                    request, 'Payment has already been made for this record.')
        else:
            messages.error(
                request, 'No records found for the specified year and month. You need to save it first!')

        return redirect('generator_month', year=year)


class OverviewYearView(View):
    template_name = 'overview.html'
    # invisible_table_template = 'overview_invisible_table.html'

    def get(self, request, *args, **kwargs):

        # Retrieve all unique valides years from the salary_items model
        validity_years = GeneratorData.objects.values_list(
            'gd_year', flat=True).distinct()
        # Retrieve all unique valides months from the GeneratorData model
        validity_months = GeneratorData.objects.values_list(
            'gd_month', flat=True).distinct()
        # Retrieve all unique valides employees from the Employees model
        validity_employees = GeneratorData.objects.values_list(
            'gd_last_name', flat=True).distinct()

        chart_data = GeneratorData.objects.all()

        unique_years = set()
        unique_months = set()
        aggregated_data = {}

        # find the maximum year in GeneratorData
        current_year = chart_data.aggregate(
            max_year=models.Max('gd_year'))['max_year']

        if current_year:
            previous_year = int(current_year) - 1
        else:
            previous_year = None

        for entry in chart_data:
            year = entry.gd_year
            month = int(entry.gd_month)
            paid_salary = entry.gd_paid_salary

            unique_years.add(year)
            unique_months.add(month)

        # Aggregate sum of gd_paid_salary for each month and year
        for item in chart_data:
            key = f"{item.gd_year}-{item.gd_month}"
            if key not in aggregated_data:
                aggregated_data[key] = 0
            aggregated_data[key] += float(item.gd_paid_salary)

        # Separate aggregated data for the current year and previous year
        aggregated_data_current_year = {}
        aggregated_data_previous_year = {}

        for key, value in aggregated_data.items():
            year, month = map(int, key.split('-'))
            if year == current_year:
                aggregated_data_current_year[month] = value
            elif year == current_year - 1:
                aggregated_data_previous_year[month] = value

        context = {'validity_years': validity_years,
                   'validity_months': validity_months,
                   'validity_employees': validity_employees,
                   'current_year': current_year,
                   'previous_year': previous_year,
                   'unique_years': sorted(unique_years),
                   'unique_months': sorted(unique_months),
                   'aggregated_data_current_year': aggregated_data_current_year,
                   'aggregated_data_previous_year': aggregated_data_previous_year}

        return render(request, self.template_name, context)


class OverviewExportView(View):
    template_name = 'overview_export.html'

    def post(self, request, *args, **kwargs):
        form = OverviewForm(request.POST)
        year = request.POST.get('year')
        month = request.POST.get('month')
        employee = request.POST.get('employee')

        # Specifing the fields for which I want to calculate the sum
        sum_fields = [
            'gd_base_monthly_salary',
            'gd_monthly_salary',
            'gd_child_allocation_1',
            'gd_child_allocation_2',
            'gd_total_monthly_wage',
            'gd_total_monthly_wage_for_social_insurance',
            'gd_total_monthly_wage_for_social_taxes',
            'gd_avs_item',
            'gd_ac_item',
            'gd_ac2_item',
            'gd_laap_item',
            'gd_laanp_item',
            'gd_laac_item',
            'gd_laace_item',
            'gd_amat_item',
            'gd_alfa_item',
            'gd_apgmal_item',
            'gd_alpetiteenfance_item',
            'gd_total_social_deduction',
            'gd_employees_phone_allocation',
            'gd_employees_representation_allocation',
            'gd_expense_report',
            'gd_public_transportation_fees',
            'gd_paid_salary',
            'gd_extraordinary_salary',
            'gd_LPP_deduction_employee',
            'gd_total_deduction_employee',
            'gd_correction_non_financial_wage',
        ]

        # Initializing an empty filter dictionary
        filter_kwargs = {}

        # Check and add filters for year, month, and employee
        if year and year.isdigit() and year != 'all':
            filter_kwargs['gd_year'] = year
        if month and month != 'all':
            filter_kwargs['gd_month'] = month
        if employee and employee != 'all':
            filter_kwargs['gd_last_name'] = employee

        # Filter the queryset based on the provided filters
        queryset = GeneratorData.objects.filter(**filter_kwargs)

        # Calculate sum for each category
        category_sums = {}
        for field_name in sum_fields:
            category_sums[field_name] = sum(
                getattr(obj, field_name, 0) for obj in queryset)

        # Convert the sums into a list of dictionaries
        category_values = [{'category': field_name, 'value': value}
                           for field_name, value in category_sums.items()]

        # Pass the category values to the invisible table template
        context = {'form': form, 'fields': category_values}
        return render(request, self.template_name, context)


class GeneratorReopenView(View):
    def post(self, request, year, month, *args, **kwargs):
        year = int(year)
        month = int(month)

        generator_data_list = GeneratorData.objects.filter(
            gd_year=year, gd_month=month)

        # Check if next month's data has been saved
        next_month = month + 1
        next_year = year
        if next_month > 12:
            next_month = 1
            next_year += 1
        
        next_month_data_exists = GeneratorData.objects.filter(gd_year=next_year, gd_month=next_month).exists()

        if next_month_data_exists:
            messages.error(request, 'Cannot reopen this month as there is a following month already saved, delete it first.')
            return redirect('generator_month', year=year)

        if generator_data_list.exists():
            if any(generator_data.gd_monthly_table_paid for generator_data in generator_data_list):
                for generator_data in generator_data_list:
                    generator_data.gd_monthly_table_paid = None
                    generator_data.save()
                messages.success(request, 'Reopen successful. The month is now available for deletion or paying.')
            else:
                messages.warning(
                    request, 'This month is not marked as paid, so it cannot be reopened.')
        else:
            messages.error(request, 'No records found for the specified year and month. You need to save it first!')
        
        return redirect('generator_month', year=year)

# A view to delete an employee
class DeleteEmployeeView(View):
    def post(self, request, pk, *args, **kwargs):
        # Get the employee instance by primary key (pk)
        employee = get_object_or_404(Employees, pk=pk)

        # Check if the employee has data in the GeneratorData model
        employee_has_data = GeneratorData.objects.filter(
            gd_title=employee.title,
            gd_first_name=employee.first_name,
            gd_last_name=employee.last_name
        ).exists()

        if employee_has_data:
            # If the employee has associated data, prevent deletion
            messages.error(request, "Cannot delete this employee as they have associated generated data.")
        else:
            # If no associated data, delete the employee
            employee.delete()
            messages.success(request, "Employee deleted successfully.")
        
        # Redirect back to the list of employees
        return redirect('Listofemployees')


# A view to delete a year
class DeleteYearView(View):
    def post(self, request, pk, *args, **kwargs):
        # Get the year instance by primary key
        year = get_object_or_404(salary_items, pk=pk)

        # Check if the year has generated data in the GeneratorData table
        year_has_data = GeneratorData.objects.filter(
            gd_year=year.validity_year
        ).exists()

        if year_has_data:
            # If the year has associated data, prevent deletion
            messages.error(request, "Cannot delete this year as it has associated generated data.")
        else:
            # If no associated data, delete the year
            year.delete()
            messages.success(request, "Year deleted successfully.")

        # Redirect back to the list of years
        return redirect('Yearview')