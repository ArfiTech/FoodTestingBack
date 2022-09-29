from msilib import Table
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import CustomerSerializer, MarketSerializer, ReviewSerializer, TableSerializer
from myapp.models import NewTable
from rest_framework.viewsets import ModelViewSet
from .models import NewTable
from .serializers import TableSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import MarketPagination, PostPageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

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
        if (NewTable.objects.filter(uuid=id)):
            data = list(NewTable.objects.filter(uuid=id))
            serializer = TableSerializer(data, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        #data = NewTable.objects.all()
        #serialized_data = TableSerializer(data, many=True)
        return HttpResponse("Not exists", status=404)

    elif request.method == 'POST':
        return HttpResponse('post')


@api_view(['POST'])
def post_api(request):
    if request.method == 'POST':
        requestedData = JSONParser().parse(request)
        serializer = TableSerializer(data=requestedData)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def postData(request):
    if request.method == 'POST':
        requestedData = JSONParser().parse(request)
        serializer = TableSerializer(data=requestedData)
        # 중복검사
        if (NewTable.objects.filter(uuid=requestedData['uuid']).exists()):
            return HttpResponse('uuid already exists', status=404)

        elif serializer.is_valid():
            serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)


@csrf_exempt
def put_api(request):
    if request.method == 'PUT':
        table_data = JSONParser().parse(request)
        table = NewTable.objects.get(uuid=table_data['uuid'])
        serializer = TableSerializer(table, data=table_data)
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse("Update Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)


@api_view(['DELETE'])
def delete_api(request, id):
    if request.method == 'DELETE':
        if (NewTable.objects.filter(uuid=id).exists()):
            table = NewTable.objects.get(uuid=id)
            table.delete()
            return JsonResponse("Delete Successfully", safe=False)
        else:
            return JsonResponse("Not exist", safe=False)
    return JsonResponse("Failed to Delete", safe=False)


# foodTesting API


def get_userinfo(request, uuid):
    if (Customer.objects.filter(uuid=uuid).exists()):
        data = list(Customer.objects.filter(uuid=uuid).values())
        # attribute -> serializer or all values()
        return JsonResponse(data, safe=False, status=200)
    return HttpResponse("Not exists", safe=False, status=404)


def modify_userinfo(request):
    table_data = JSONParser().parse(request)
    table = Customer.objects.get(uuid=table_data['uuid'])
    serializer = CustomerSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse("Update Successfully", safe=False)
    return JsonResponse("Failed to Update", safe=False)


def register_userinfo(request):
    requestedData = JSONParser().parse(request)
    serializer = CustomerSerializer(data=requestedData)
    if (Customer.objects.filter(email=requestedData['email']).exists()):
        return HttpResponse('email is already exists', status.HTTP_400_BAD_REQUEST)
    elif (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse("Failed to Add", safe=False, status=status.HTTP_404_NOT_FOUND)


def post_review(request):
    requestedData = JSONParser().parse(request)
    serializer = ReviewSerializer(data=requestedData)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse("Failed to add", safe=False, status=status.HTTP_404_NOT_FOUND)


class getStoreInfobyRegNum(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        regnum = self.kwargs['regnum']
        return Market.objects.filter(reg_num=regnum)


class getStoreInfobyUUID(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        id = self.kwargs['uuid']
        return Market.objects.filter(customer_uuid=id)


def modify_storeInfo(request):
    requestedData = JSONParser().parse(request)
    serializer = MarketSerializer(data=requestedData)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse("Failed to add", safe=False, status=status.HTTP_404_NOT_FOUND)
