from django.contrib import admin
from django.urls import path
# from .views import DataListAPI
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    # path('api/', DataListAPI.as_view()),
    path('register/userinfo', views.register_userinfo),
    path('get/userinfo/<str:uuid>', views.get_userinfo),
    path('modify/userinfo', views.modify_userinfo),
    path('post/review', views.post_review),
    path('marketinfo/by-registartion-num/<str:regnum>',
         views.getMarketInfobyRegNum.as_view()),
    path('marketinfo/by-customer-id/<str:uuid>',
         views.getMarketInfobyUUID.as_view()),
    path('modify/marketinfo', views.modify_marketInfo),
]