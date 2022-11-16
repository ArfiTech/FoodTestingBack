from django.contrib import admin
from django.urls import path, re_path, include
# from .views import DataListAPI
from django.conf import settings
from django.conf.urls.static import static
from app import views
from rest_framework.routers import SimpleRouter
from .views import DropBoxViewset

router = SimpleRouter()
router.register('accounts', DropBoxViewset, 'Drop Boxes')

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
    path('register/store', views.register_marketInfo),
    path('modify/storeinfo', views.modify_marketInfo),
    path('post/new-menu', views.post_menu),
    path('delete/menu/<str:regnum>&<str:uuid>', views.delete_menu),
    re_path(r'^marketinfo/orderby/distance/(?P<category>\w+)/(?P<lat>\d+\.\d+)&(?P<lng>\d+\.\d+)$',
            views.get_marketInfo_orderBy_distance),
    path('get/selected-questions/<str:reg_num>', views.getReviewQuestions),
    path('register/selected-question', views.registerQuestions),
    path('post/question/written-by-owner', views.postReviewQuestions),
    path('get/default/question/<int:type>', views.getDefaultQuestions),
    # path('get/question/written-by-owner/<str:reg_num>', views.getQuesMadebyMarket),
    path('post/reviews', views.postReviews),
    path('get/reviews/written-by-customer/<str:reg_num>', views.getReviewAnswers),
    # path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo),
    path('post/overall-selected-questions', views.registerOverallQues),
    path('', include(router.urls)),
    path('post/img', views.postImg)
]
