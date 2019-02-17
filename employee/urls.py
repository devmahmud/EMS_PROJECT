from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('<int:emp_id>/', views.employee_detail, name='employee_detail'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:emp_id>', views.edit_employee, name='edit_employee'),
    path('delete/<int:emp_id>', views.delete_employee, name='delete_employee'),
]
