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
]
