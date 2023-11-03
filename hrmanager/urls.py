from . import views
from django.urls import path


urlpatterns = [
    path('', views.EmployeesList.as_view(), name='home'),
]