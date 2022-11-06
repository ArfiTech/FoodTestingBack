from django.contrib import admin
from django.urls import path, re_path
# from .views import DataListAPI
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    # foodTesting project API

    path('login/email=<str:email>&pw=<str:pw>', views.login_user),
    path('register/userinfo', views.register_userinfo),
    path('get/userinfo/<str:uuid>', views.get_userinfo),
    path('modify/userinfo', views.modify_userinfo),
    path('post/review', views.post_review),
    path('storeinfo/by-registartion-num/<str:regnum>',
         views.getMarketInfoWithPost),
    path('storeinfo/by-customer-id/<str:uuid>',
         views.getMarketInfobyUUID),
    path('marketinfo/<str:category>', views.getMarketInfobyCategory.as_view()),
    path('modify/storeinfo', views.modify_marketInfo),
    path('post/new-menu', views.post_menu),
    path('delete/menu/<str:regnum>&<str:uuid>', views.delete_menu),
    re_path(r'^marketinfo/orderby/distance/(?P<category>\w+)/(?P<lat>\d+\.\d+)&(?P<lng>\d+\.\d+)$',
            views.get_marketInfo_orderBy_distance),
    #path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo),
]
