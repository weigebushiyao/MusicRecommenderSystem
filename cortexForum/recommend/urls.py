# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^recommend/item$', views.itemRecommend, name='item_recommend'),
]
