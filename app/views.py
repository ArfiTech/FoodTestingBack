from django.shortcuts import render

# Create your views here.
from msilib import Table
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import TableSerializer
from app.models import NewTable
from rest_framework.viewsets import ModelViewSet
from .models import NewTable
from .serializers import TableSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import PostPageNumberPagination
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def showData(request):
    data = list(NewTable.objects.values())
    return JsonResponse(data, safe=False)


# ListAPIView를 이용한 pagination/filter

class PostViewSet(ListAPIView):
    #queryset = NewTable.objects.all()
    serializer_class = TableSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        customer = self.kwargs['name']
        return NewTable.objects.filter(name=customer)


# api_view를 이용한 get, post method 정의
@api_view(['GET', 'POST'])
def get_api(request, id):
    if request.method == 'GET':
        data = list(NewTable.objects.filter(uuid=id).values())
        #data = NewTable.objects.all()
        #serialized_data = TableSerializer(data, many=True)
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        return HttpResponse('post')


@api_view(['POST'])
def post_api(request):
    if request.method == 'POST':
        print('post method')
        print(request.data)
        serializer = TableSerializer(data=request.data, many=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)