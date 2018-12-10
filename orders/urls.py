from django.urls import path
from . import views
from django.conf.urls import url

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.cust_order, name='cust_order_detail'),
    path('order/<int:order_id>/pdf', views.cust_order_pdf, name='cust_order_pdf'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/(<int:order_id>)/pdf',  views.admin_order_pdf, name='admin_order_pdf'),

    #url(r'^admin/order/(?P<order_id>\d+)/pdf/$',  views.admin_order_pdf, name='admin_order_pdf'),
]
