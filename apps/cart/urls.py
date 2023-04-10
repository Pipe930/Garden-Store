from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlsCart = [
    path('', views.CartsListView.as_view(), name='carts'),
    path('cart/<int:id>', views.CartDetailView.as_view(), name='cart'),
    path('cart/user/<int:idUser>', views.CartUserView.as_view(), name='cartuser'),
    path('cart/create', views.CreateCartView.as_view(), name='createcart'),
    path('item/add', views.AddCartItemView.as_view(), name='additem'),
    path('item/substract', views.SubtractCartItemView.as_view(), name='substractitem')
]

urlsCart = format_suffix_patterns(urlsCart)