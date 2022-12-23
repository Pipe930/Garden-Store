from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsCategory = [
    path('', views.CategoryListView.as_view(), name='categories'),
    path('category/<int:id>', views.CategoryDetailView.as_view(), name='category'),
]

urlsCategory = format_suffix_patterns(urlsCategory)

