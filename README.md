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
