from django.urls import path, re_path
from myapp import views
urlpatterns = [
    path('', views.showData),
    path('test/<int:id>', views.get_api),
    # post 아직 실행 안됨
    path('post', views.post_api),
    path('post2', views.postData),
    path('put', views.put_api),
    path('delete/<int:id>', views.delete_api),
    # http://127.0.0.1:8000/<str:name>?page=1
    path('<str:name>', views.PostViewSet.as_view()),

    # foodTesting project API

    path('login/email=<str:email>&pw=<str:pw>', views.login_user),
    path('register/userinfo', views.register_userinfo),
    path('get/userinfo/<str:uuid>', views.get_userinfo),
    path('modify/userinfo', views.modify_userinfo),
    path('storeinfo/by-registartion-num/<str:regnum>',
         views.getMarketInfoWithPost),
    path('storeinfo/by-customer-id/<str:uuid>',
         views.getMarketInfobyUUID),
    path('storeinfo/<str:category>', views.getMarketInfobyCategory.as_view()),
    path('register/store', views.register_marketInfo),
    path('modify/storeinfo', views.modify_marketInfo),
    path('post/new-menu', views.post_menu),
    path('modify/menu', views.modify_menu),
    path('delete/menu/<str:regnum>&<str:uuid>', views.delete_menu),
    re_path(r'^marketinfo/orderby/distance/(?P<category>\w+)/(?P<lat>\d+\.\d+)&(?P<lng>\d+\.\d+)$',
            views.get_marketInfo_orderBy_distance),
    path('get/selected-questions/<str:reg_num>', views.getReviewQuestions),
    path('register/selected-question', views.registerQuestions),
    path('post/question/written-by-owner', views.postReviewQuestions),
    path('get/default/question/<int:type>', views.getDefaultQuestions),
    path('post/reviews', views.postReviews),
    path('get/reviews/written-by-customer/<str:reg_num>', views.getReviewAnswers),
    #path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo),
    path('post/overall-selected-questions', views.registerOverallQues),
    path('get/review-research/<str:regnum>', views.getReviewResearch),
    re_path(r'^get/main/new-market/(?P<lat>\d+\.\d+)&(?P<lng>\d+\.\d+)$',
            views.getNewMarket),
    path('get/main/new-menu', views.getNewMenu)
]
