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

    # uuid로 회원정보를 가져오는 요청
    path('register/userinfo', views.register_userinfo),
    path('get/userinfo/<str:uuid>', views.get_userinfo),
    path('modify/userinfo', views.modify_userinfo),
    path('post/review', views.post_review),
    path('storeinfo/by-registartion-num/<str:regnum>',
         views.getMarketInfoWithPost),
    path('storeinfo/by-customer-id/<str:uuid>',
         views.getMarketInfobyUUID.as_view()),
    path('storeinfo/<str:category>', views.getMarketInfobyCategory.as_view()),
    path('modify/storeinfo', views.modify_marketInfo),
    path('post/new-menu', views.post_menu),
    path('delete/menu/<str:regnum>&<str:uuid>', views.delete_menu),
    re_path(r'^marketinfo/orderby/distance/(?P<category>\w+)/(?P<lat>\d+\.\d+)&(?P<lng>\d+\.\d+)$',
            views.get_marketInfo_orderBy_distance),
    #path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo),
]
