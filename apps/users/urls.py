from django.urls import path
from . import views

urlsUsers = [
    path('', views.UsersListView.as_view(), name='users'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout')
]