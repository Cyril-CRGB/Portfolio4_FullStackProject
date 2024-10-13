This is a web app for generating swiss salaries of a small sized company.

The site is live here : https://portfolio4-fullstackproject-67b0ea26bc65.herokuapp.com/

Credentials for visitors
user: Administrator1
Password: br5*9v/iOG;6

Input validation Enhancements summary:
 - Added form-level validations using clean() methods in forms.
 - Implemented model-level validations for added security, ensuring fields have appropriate constraints.
 - Added error messages and validation handling in views using form_invalid() and form_valid() to guide users.
 - Modified templates to properly display error messages to users.
 - Created database constraints and custom signals to prevent inconsistencies even outside of form usage.


 buggs.

 i had to delete all migrations made, because i changed it, then received this message: "You are trying to change the nullable field 'start_date' on employees to non-nullable without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:" and gave it a wrong default value

parsing dates + date format

python manage.py makemigrations
python manage.py migrate

url name='generator_year' gave a mistake when no years was populated by user first: deal with the error by setting default values to 0 and adding messages
