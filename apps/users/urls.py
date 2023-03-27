from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsUsers = [
    path('', views.UsersListView.as_view(), name='users'),
    path('user/<int:id>', views.UserView.as_view(), name='user'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('subscriptions/', views.SubscripcionListView.as_view(), name='subscriptions'),
    path('subscriptions/user/<int:id>', views.SubscriptionDetailView.as_view(), name='subscription'),
    path('sendEmail', views.SendEmailView.as_view(), name='sendemail'),
    path('change-password', views.ChangePasswordView.as_view(), name='changepassword')

]

urlsUsers = format_suffix_patterns(urlsUsers)