# Importing the necessary modules or classes
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import Employees
from django.http import HttpRequest
from datetime import date


# Test EmployeesAdmin in admin.py
class TestEmployeesAdmin(TestCase):
    # Create a clean and consistent environnement for the test case, that avoids code duplication and ensure that each test method starts with the same initial conditions
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass', email='testuser@example.com')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        # Create some test Employees instances
        self.employee1 = Employees.objects.create(
            title='Employee1', last_name='Doe', first_name='John', employees_status=0, social_security_number=1312111098765)
        self.employee2 = Employees.objects.create(
            title='Employee2', last_name='Smith', first_name='Jane', employees_status=1, social_security_number=1312111098764)

    def test_deactivate_employee_action(self):
        # Action to deactivate employee
        response = self.client.post(
            # Replace with the actual app name
            reverse('admin:hrmanager_employees_changelist'),
            {'action': 'deactivate_employee',
                '_selected_action': [str(self.employee1.id)]}
        )

        # Check if the status is updated
        self.employee1.refresh_from_db()
        # Expecting 1 for inactive status
        self.assertEqual(self.employee1.employees_status, 1)

    def test_activate_employee_action(self):
        # Action to activate employee
        response = self.client.post(
            # Replace with the actual app name
            reverse('admin:hrmanager_employees_changelist'),
            {'action': 'activate_employee',
                '_selected_action': [str(self.employee2.id)]}
        )

        # Check if the status is updated
        self.employee2.refresh_from_db()
        # Expecting 0 for active status
        self.assertEqual(self.employee2.employees_status, 0)
