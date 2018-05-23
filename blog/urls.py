from django.conf.urls import url
from . import *
from . import views

urlpatterns = [
    url(r'^$', views.price_coin, name='index'),
    url(r'^index', views.price_coin, name='index'),
    # url(r'^btc/$', views.view_price, name='view_price'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.message),
    url(r'^jpy', views.jpy_list, name='jpy'),
    url(r'^coin', views.rsi_list, name='coin'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^about', views.about, name='about'),
]
