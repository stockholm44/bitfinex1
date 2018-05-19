from django.conf.urls import url
from . import *
from . import views

urlpatterns = [
    url(r'^$', views.price_coin, name='price_coin'),
    # url(r'^btc/$', views.view_price, name='view_price'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.message),
    url(r'^jpy_list/', views.jpy_list, name='jpy_list'),
    url(r'^rsi_list/', views.rsi_list, name='rsi_list'),

]
