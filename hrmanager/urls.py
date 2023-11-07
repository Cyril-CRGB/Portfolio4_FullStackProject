from . import views
from django.urls import path


urlpatterns = [
    # path('', HomeView, name='home')
    path('', views.HomeView.as_view(), name='home'),
    path('employees/', views.EmployeesList.as_view(), name='Listofemployees'),
    path('employeesdetail/', views.EmployeesDetail.as_view(), name='Detailofemployees'),
]
