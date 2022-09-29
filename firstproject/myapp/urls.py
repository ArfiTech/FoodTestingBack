from django.urls import path
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
         views.getStoreInfobyRegNum.as_view()),
    path('storeinfo/by-customer-id/<str:uuid>',
         views.getStoreInfobyUUID.as_view()),
    path('modify/storeinfo', views.modify_storeInfo),
    #path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo)
]
