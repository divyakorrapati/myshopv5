from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('shop.urls', namespace='shop')),
url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    #url(r'^login/$', views.login, name='login'),
    #url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    #re_path(r'^accounts/login/$', LoginView.as_view(template_name='regiatration/login.html'), name="login"),
    #re_path(r'^accounts/logout/$', LogoutView.as_view(), LogoutView.next_page, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
