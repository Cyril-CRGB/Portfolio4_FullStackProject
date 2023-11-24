from . import views
from django.urls import path


urlpatterns = [
    # path('', HomeView, name='home')
    path('', views.HomeView.as_view(), name='home'),
    path('employees/', views.EmployeesList.as_view(), name='Listofemployees'),
    # path('employeesdetail/', views.EmployeesDetail.as_view(), name='Detailofemployees'),
    path('employee/<int:pk>/', views.EnployeeDetailView.as_view(),
         name='Detailofemployees'),
    path('employee/new/', views.EnployeeAddView.as_view(),
         name='Addanemployees'),
    path('employee/<int:pk>/modify/', views.ModifyEmployeeView.as_view(),
         name='modify_employee'),
    path('years/', views.YearList.as_view(),
         name='Yearview'),
    path('year/<int:pk>/', views.YearDetailView.as_view(),
         name='Detailofyears'),
    path('year/new/', views.YearAddView.as_view(),
         name='Addayear'),
    path('year/<int:pk>/modify/', views.ModifyYearView.as_view(),
         name='modify_year'),
    path('generator/', views.GeneratorYearView.as_view(), name='generator_year'),
    path('generator/<int:year>/',
         views.GeneratorMonthView.as_view(), name='generator_month'),
    path('generator/<int:year>/<int:month>/employees/',
         views.GeneratorEmployeesView.as_view(), name='generator_employees'),
    path('generator/<int:year>/<int:month>/monthly-table/',
         views.GeneratorMonthlyTableView.as_view(), name='generator_monthly_table'),

]
