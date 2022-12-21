from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsIndex = [
    path('', views.IndexView.as_view())
]

urlsIndex = format_suffix_patterns(urlsIndex)