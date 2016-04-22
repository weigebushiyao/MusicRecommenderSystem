# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^recommend/item$', views.itemRecommend, name='item_recommend'),
    url(r'^recommend/result/(?P<recommend_music>).*$',views.itemRecommend,name='recommend_result')
]
