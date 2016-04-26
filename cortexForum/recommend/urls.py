# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^recommend/item$', views.itemRecommend, name='item_recommend'),
    url(r'^recommend/result$',views.recommend_result,name='recommend_result'),
    url(r'^recommend/result/check$',views.recommend_result_check,name='recommend_result_check'),
]
