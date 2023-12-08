# Importing the necessary modules or classes
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import Employees
from django.http import HttpRequest

# Test EmployeesAdmin in admin.py


class TestEmployeesAdmin(TestCase):
    # Create a clean and consistent environnement for the test case, that avoids code duplication and ensure that each test method starts with the same initial conditions
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        # Create some test Employees instances
        self.employee1 = Employees.objects.create(
            last_name='Doe', first_name='John', employees_status=0)
        self.employee2 = Employees.objects.create(
            last_name='Smith', first_name='Jane', employees_status=1)

    def test_deactivate_employee_action(self):
        # Get the URL for the change page of the first employee
        url = reverse('admin:yourapp_employees_change',
                      args=[self.employee1.id])

        # Get the CSRF token by making a GET request to the change page
        response = self.client.get(url)
        csrf_token = response.cookiest['csrftoken'].value

        # Perform a POST request to the "deactivate_employee" action
        response = self.client.post(url, {
            'action': 'deactivate_employee',
            '_selected_action': [self.employee1.id],
            'csrfmiddlewaretoken': csrf_token
        }, follow=True)

        # Check that the employee's status has been updated to 1 (deactivated)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.employees_status, 1)

        # Check the response to ensure success (HTTP status code 200)
        self.assertEqual(response.status_code, 200)

        # Check that the success message is present in the response content
        self.assertContains(response, 'Succesfully deactivated 1 employee.')

    def test_activate_employee_action(self):
        # Get the URL for the change page of the second employee
        url = reverse('admin:yourapp_employees_change',
                      args=[self.employee2.id])

        # Get the CSRF token by making a GET request to the change page
        response = self.client.get(url)
        csrf_token = response.cookiest['csrftoken'].value

        # Perform a POST request to the "activate_employee" action
        response = self.client.post(url, {
            'action': 'activate_employee',
            '_selected_action': [self.employee2.id],
            'csrfmiddlewaretoken': csrf_token
        }, follow=True)

        # Check that the employee's status has been updated to 0 (activated)
        self.employee2.refresh_from_db()
        self.assertEqual(self.employee2.employees_status, 0)

        # Check the response to ensure success (HTTP status code 200)
        self.assertEqual(response.status_code, 200)

        # Check that the success message is present in the response content
        self.assertContains(response, 'Successfully activated 1 employee.')
