from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('order/<int:order_id>/', views.cust_order_detail, name='cust_order_detail'),
    path('order/<int:order_id>/pdf', views.cust_order_pdf, name='cust_order_pdf')
]