from django.test import TestCase, Client
from . import views
from django.urls import reverse
from .models import Employees
from .forms import ModifyEmployeeForm


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
        # Call the parent class's setUp method
        super().setUp()
        # Create an instance of the Employees model for testing
        self.employee = Employees.objects.create(
            title='Mr.',
            first_name='Mad',
            last_name='Max',
            employees_gender='M',
            employees_marital_status='S',
            social_security_number='1234567890123',
        )

    def test_modify_employee_view(self):
        # Use the Django test client to simulate a GET request to the ModifyEmployeeView
        response = self.client.get(
            reverse('modify_employee', args=[self.employee.pk]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verify that the correct employee instance is in the context
        self.assertEqual(response.context['object'], self.employee)

        # Simulate a POST request to the ModifyEmployeeview with updated data
        updated_data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
        }

        response = self.client.post(reverse('modify_employee', args=[
                                    self.employee.pk]), updated_data, follow=True)

        # Check that the response status code is a redirect (302) indicating a successful form submission
        self.assertEqual(response.status_code, 302)

        # Retrieve the updated employee instance from the database
        updated_employee = Employees.objects.get(pk=self.employee.pk)

        # Check if the employee instance has been updated with the new data
        self.assertEqual(updated_employee.first_name, 'Updated First Name')
        self.assertEqual(updated_employee.last_name, 'Updated Last Name')

        # Check the final redirect URL after a successful form submission
        expected_redirect_url = reverse(
            'Detailofemployees', kwargs={'pk': updated_employee.pk})
        self.assertRedirects(response, expected_redirect_url, status_code=302)
