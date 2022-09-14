from django.urls import path
from .views import DataListAPI

urlpatterns = [
    path('api/', DataListAPI.as_view()),
]