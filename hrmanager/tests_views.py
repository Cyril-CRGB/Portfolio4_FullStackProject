# Importing the necessary modules or classes
from django.test import TestCase, Client, RequestFactory
from . import views
from django.urls import reverse
from .models import Employees, salary_items, GeneratorData
from .forms import ModifyEmployeeForm
from django.shortcuts import get_object_or_404
from hrmanager.views import ModifyEmployeeView, YearDetailView


class TestHomeView(TestCase):
    def setUp(self):
        # Create a Django test client
        self.client = Client()

    def test_get(self):
        # Use the Django test client to simulate a GET request to the HomeView
        response = self.client.get(reverse('home'))
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)


class TestEmployeeDetailView(TestCase):
    def setUp(self):
        # Create an instance of the Employees model for testing
        self.employee = Employees.objects.create(
            title='Mr.',
            first_name='Mad',
            last_name='Max',
            employees_gender='M',
            employees_marital_status='S',
            social_security_number='1234567890123',
        )

    def test_get_context_data(self):
        # Use the Django test client to simulate a GET request to the EmployeeDetailView
        response = self.client.get(
            reverse('Detailofemployees', args=[self.employee.pk]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check the context data returned by the view
        selected_employee = response.context['selected_employee']
        selected_employee_pk = response.context['selected_employee_pk']

        # Verify that the correct employee instance is in the context
        self.assertEqual(selected_employee, self.employee)

        # Verify that the 'selected_employee_pk' context variable is set correctly
        self.assertEqual(selected_employee_pk, self.employee.pk)


class TestModifyEmployeeView(TestCase):
    def setUp(self):
        # Create an instance of the Employees model for testing
        self.employee = Employees.objects.create(
            title='Mr.',
            first_name='Mad',
            last_name='Max',
            employees_gender='M',
            employees_marital_status='S',
            social_security_number='1234567890000',
        )

    def test_get_object(self):
        # Create a ModifyEmployeeView instance
        view_instance = ModifyEmployeeView()

        # Set the view's request attribute manually
        view_instance.request = None

        # Set the view's kwargs attribute manually
        view_instance.kwargs = {'pk': self.employee.pk}

        # Retrieve the employee instance using get_object_or_404
        employee_from_view = view_instance.get_object()

        # Check that the retrieved object is the same as the one created in setUp
        self.assertEqual(employee_from_view, self.employee)

    def test_get_context_data(self):
        # Create a ModifyEmployeeVeiw instance
        view_instance = ModifyEmployeeView()

        # Create a mock request using Django's RequestFactory
        request = RequestFactory().get('/fake-url/')
        view_instance.request = request

        # Set the view's object attribute manually (since it's not set by the URL routing in the test)
        view_instance.object = self.employee

        # Call the get_conext_data method
        context = view_instance.get_context_data()

        # Check that the context contains the expected values
        self.assertEqual(context['current_pk'], self.employee.pk)
        self.assertEqual(context['form'].instance, self.employee)

    def test_get_success_url(self):
        # Create a ModifyeEmployeeView instance
        view_instance = ModifyEmployeeView()

        # Set the view's kwargs manually
        view_instance.kwargs = {'pk': self.employee.pk}

        # Call the get_success_url method
        success_url = view_instance.get_success_url()

        # Check that the generated URL is correct
        expected_url = reverse('Detailofemployees', kwargs={
                               'pk': self.employee.pk})
        self.assertEqual(success_url, expected_url)


class TestYearDetailView(TestCase):
    def setUp(self):
        # Create an instance of te salary_items model for testing
        self.year_item = salary_items.objects.create(
            validity_year='2023',
            avs_item=0.0,
            ac_item=0.0,
            ac2_item=0.0,
            laap_item=0.0,
            laanp_item=0.0,
            laac_item=0.0,
            laace_item=0.0,
            amat_item=0.0,
            alfa_item=0.0,
            apgmal_item=0.0,
            alpetiteenfance_item=0.0,
            child_alloc_1_item=0.0,
            child_alloc_2_item=0.0,)

    def test_get_context_data(self):
        # Create a YearDetailView instance
        view_instance = YearDetailView()

        # Set the view's object attribute manually
        view_instance.object = self.year_item

        # Call the get_context_data method
        context = view_instance.get_context_data()

        # Check th1at the context contains the expected values
        self.assertEqual(context['selected_year_pk'], self.year_item.pk)
