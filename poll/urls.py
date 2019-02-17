from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='poll_list'),
    path('<int:poll_id>/details/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/', views.poll, name='single_poll'),
]
