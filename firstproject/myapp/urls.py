from django.urls import path
from myapp import views
urlpatterns = [
    path('', views.showData),
    path('test/<int:id>', views.get_api),
    path('test/post', views.post_api),

    # http://127.0.0.1:8000/page/?page=1
    path('page/', views.PostViewSet.as_view())
]
