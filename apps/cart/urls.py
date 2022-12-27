from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlsCart = [
    path('', views.CartsListView.as_view(), name='carts'),
    path('cart/<int:id>', views.CartDetailView.as_view(), name='cart'),
]

urlsCart = format_suffix_patterns(urlsCart)