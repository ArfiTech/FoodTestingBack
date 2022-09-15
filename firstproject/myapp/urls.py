from django.urls import path
from myapp import views
urlpatterns = [
    path('', views.showData),
    path('test/<int:id>', views.get_api),
    # post 아직 실행 안됨
    path('post', views.post_api),
    path('post2', views.postData),
    # http://127.0.0.1:8000/<str:name>?page=1
    path('<str:name>', views.PostViewSet.as_view()),

    # foodTesting project API

    # uuid로 회원정보를 가져오는 요청
    path('get/userinfo/<str:uuid>', views.get_userinfo),
    #path('storeinfo/by-registartion-num/<str:regnum>', views.get_storeinfo)
]
