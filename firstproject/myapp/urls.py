from django.urls import path
from myapp import views
urlpatterns = [
    path('', views.showData),
    path('test/<int:id>', views.get_api),
    # post 아직 실행 안됨
    path('test/post', views.post_api),

    # http://127.0.0.1:8000/<str:name>?page=1
    path('<str:name>', views.PostViewSet.as_view())
]
