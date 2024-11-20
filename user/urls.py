from os import name

from django.urls import path, include

from user import views

urlpatterns = [
    # path('list-box/', views.listBox),   
    path('validateUser/', views.UsersDetail),   
]