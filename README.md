# Django Payroll Management System

## Description
The Django Payroll Management System is a web-based application designed to manage employee payroll, salary and related data. 
It includes features such as employee management, salary year configuration, salary data generation, and reports for both current and previous years. A **export** in excel is also possible. This project leverages Django for backend processing and database management, and uses templates for the fronted user interface.

This app is called 'HR MANAGER' and it is part of a larger project called 'OCTOPUS', have a look at the schematic:

<img src="images/1_printscreen_Readme.jpeg" alt="ReadmePicture1">

## Features
<img src="images/2_printscreen_Readme.jpg" alt="ReadmePicture2">

- Employees: Add, modify, and delete employees. Employees can be marked as active or inactive. 
    *(for modification and deletion, only possible if no data is generated for it.)*
- Year: Add, modify, and delete years.
    *(for modification and deletion, only possible if no data is generated for it.)*
- Generator: Generate monthly salary data for active employees, with the ability to save, modify, delete, pay, and reopen for each month of the year.
- Overview: View aggregated data in charts to compare salary data over different months and years, you also have the possiblity to export in excel.

As it is a Process oriented app, you need to create 'Employees' and 'Years' before generating any salary and overviewing them. Moreover you need to go through specific steps in order to achieve the payroll monthly job. 

### First view the list of employees
<img src="images/3_printscreen_Readme.jpg" alt="ReadmePicture3">

You can see [active] as well as [inactive] employees. You can 'See detail', 'Modify' and 'Delete' every employee under the condition that they were not already 'paid'. You have also the possibility to 'Add a new employee'. All CRUD (Create/Read/Update/Delete), data validation for forms as well as messaging to the client are properly handled, in order to offer the best client experience.   

Here you will be able to save personal information, like the name, gender, marital status, age, day of birth, but also the wages elements of the employee. These information will be used for each run of the monthly salary process. 

### Second view the list of years
<img src="images/4_printscreen_Readme.jpg" alt="ReadmePicture4">

You can see each year that you created. You can 'See detail', 'Modify' and 'Delete' every year, under the condition that this year as not been used already. You have also the possibility to 'Add a new year'. All CRUD (Create/Read/Update/Delete), data validation for forms as well as messaging to the client are properly handled, in order to offer the best client experience. 

Here you will be able to save global information, like the rates for each social insurance the employer need to pay. These information will be used for each run of the monthly salary process. 

### Third, the salary process in itself

#### Select the year
<img src="images/5_printscreen_Readme.jpg" alt="ReadmePicture5">

You can see each year that you created under the second step. You also can see whether the year is **Completed** (all 12 months have been 'paid'), **Current** (not all, can also be zero, meaning next process in line) or **Not available** (it does not make sense to be able to pay february 2026, when november 2025 has not been 'paid')

#### Select the month
<img src="images/6_printscreen_Readme.jpg" alt="ReadmePicture6">

You can see that the current month is 'March'. You can *Save* / *Delete* / *Pay* but not yet *See* (since nothing has been calculated yet, calculation is triggered when the client click on *Save*). 

Badges on the left indicate, whether the salaries have been 'Paid' **Green** or 'calculated/saved' **Blue** or 'not yet' **White**. 

'April' is the next month and we can read "this period is not available", as we already said this process oriented app needs the client to go month to month which is usercase relevant. 

Once the salaries have been 'Paid' (**Green** badge), two other button come up: 'reopen' and 'See'. You can 'reopen' the very last 'Paid' salary, here 'February' and go through the same process again after modifying 'Year' rates (appart form the 'year' itself if already used in a process) or 'Employees' informations (appart from the 'title' if already used in a process). 

All CRUD (Create/Read/Update/Delete), data validation for forms as well as messaging to the client are properly handled, in order to offer the best client experience. 

<img src="images/7_printscreen_Readme.jpg" alt="ReadmePicture7">

Once 'Pay' as been click we see the badge of the concerned month become **Green** and the previously 'not available' month become 'available' with all the button for CRUD. 'March' is now ready to be 'reopened' or 'Seen'. 

<img src="images/8_printscreen_Readme.jpg" alt="ReadmePicture8">

#### Overview the data
<img src="images/9_printscreen_Readme.jpg" alt="ReadmePicture9">

You can watch the progression of the wages over the span of two consecutive years. If you click on 'View aggregated Data' (which you can filter with the help of the three lists: 'Year', 'Month' and 'Employee') you can access a table showing all calculation, you can also export the table in excel. 

<img src="images/10_printscreen_Readme.jpg" alt="ReadmePicture10">





The site is live here : https://portfolio4-fullstackproject-67b0ea26bc65.herokuapp.com/

Credentials for visitors
user: Admin
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
