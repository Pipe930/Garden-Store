from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlsCategory = [
    path('', views.ListCategoriesView.as_view(), name='categories'),
    path('created', views.CreateCategoryView.as_view(), name='createdcategory'),
    path('category/<int:id>', views.CategoryDetailView.as_view(), name='category'),
    path('category/update/<int:id>', views.UpdateCategoryView.as_view(), name='updatecategory'),
    path('category/delete/<int:id>', views.DeleteCategoryView.as_view(), name='deletecategory'),
]

urlsOffer = [
    path('', views.OfferListView.as_view(), name='offers'),
    path('offer/<int:id>', views.OfferDetailView.as_view(), name='offer')
]

urlsProduct = [
    path('', views.ListProductsView.as_view(), name='products'),
    path('created', views.CreateProductView.as_view(), name='createproduct'),
    path('product/<int:id>', views.ProductDetailView.as_view(), name='product'),
    path('product/<str:slug>', views.ProductView.as_view(), name='productslug'),
    path('product', views.ProductSearchView.as_view(), name='searchproduct'),
    path('offer/', views.ProductOfferView.as_view(), name='productoffer'),
    path('category/<int:id>', views.ProductFilterView.as_view(), name='productfilter')
]

urlsCategory = format_suffix_patterns(urlsCategory)
urlsOffer = format_suffix_patterns(urlsOffer)
urlsOffer = format_suffix_patterns(urlsProduct)
