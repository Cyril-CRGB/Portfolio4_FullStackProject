from django.test import TestCase
from .models import Employees, salary_items


# Test the model 'Employees'
class TestEmployeesModel(TestCase):
    # Create a clean and consistent environnement for the test case, that avoids code duplication and ensure that each test method starts with the same initial conditions
    def setUp(self):
        # Create an instance of the Employees model for testing
        self.employee = Employees(
            title='Mr.',
            first_name='Mad',
            last_name='Max',
            employees_gender='M',
            employees_marital_status='S',
            social_security_number='1234567890123',
        )

    def test_employee_str_method(self):
        # Test that the __str__ method returns the expected string
        expected_str = 'Mr.'
        self.assertEqual(str(self.employee), expected_str)


# Test the model 'Salary_items'
class TestSalaryItemsModel(TestCase):
    def setUp(self):
        # Create an instance of the salary_items model for testing
        self.salary_item = salary_items.objects.create(
            validity_year='1914',
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
            child_alloc_2_item=0.0,
        )

    def test_str_method(self):
        # Test the __str__ method to ensure it returns the expected string
        expected_str = '1914'
        self.assertEqual(str(self.salary_item), expected_str)
