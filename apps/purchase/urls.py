from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlsVoucher = [
    path('', views.OrderView.as_view(), name='vourchers'),
    path('user/<int:idUser>', views.OrderUserDetailView.as_view(), name='detailvoucher')
]

urlsTicker = [
    path('', views.TicketView.as_view(), name='tickets'),
    path('user/<int:idUser>', views.TicketUserView.as_view(), name='detailticket')
]

urlsVoucher = format_suffix_patterns(urlpatterns=urlsVoucher)