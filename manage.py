#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the default settings module for my Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octopus.settings')
    try:
        # Import the Django management command-line utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an error if Django isn't installed or the irtual environment isn't activated
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line utility with the arguments passed to the script
    execute_from_command_line(sys.argv)

# Check if this script is being run directly (not imported as a module)
if __name__ == '__main__':
    main()
