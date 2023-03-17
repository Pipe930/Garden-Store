from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsCategory = [
    path('', views.CategoryListView.as_view(), name='categories'),
    path('category/<int:id>', views.CategoryDetailView.as_view(), name='category'),
]

urlsOffer = [
    path('', views.OfferListView.as_view(), name='offers'),
    path('offer/<int:id>', views.OfferDetailView.as_view(), name='offer')
]

urlsProduct = [
    path('', views.ProductsGenericView.as_view(), name='products'),
    path('product/<int:id>', views.ProductDetailView.as_view(), name='product'),
    path('product/<str:slug>', views.ProductView.as_view(), name='productslug'),
    path('product', views.ProductSearchView.as_view(), name='searchproduct')
]

urlsCategory = format_suffix_patterns(urlsCategory)
urlsOffer = format_suffix_patterns(urlsOffer)
urlsOffer = format_suffix_patterns(urlsProduct)

