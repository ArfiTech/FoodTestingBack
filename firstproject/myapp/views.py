from msilib import Table
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import CustomerSerializer, MarketSerializer, PostSerializer, ReviewSerializer, TableSerializer
from myapp.models import NewTable, Customer, Market, Post, Questionlist, Review
from rest_framework.viewsets import ModelViewSet
from .models import NewTable
from .serializers import TableSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import MarketPagination, PostPageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import models
from django.db.models.expressions import RawSQL
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


# getMarketInfobyRegNum + menu까지


def getMarketInfoWithPost(request, regnum):
    marketInfo = list(Market.objects.filter(reg_num=regnum).values())
    postInfo = list(Post.objects.filter(write_market=regnum).values())
    return JsonResponse({"market": marketInfo, "post": postInfo}, safe=False, status=status.HTTP_200_OK)


class getMarketInfobyUUID(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        id = self.kwargs['uuid']
        return Market.objects.filter(customer_uuid=id)


class getMarketInfobyCategory(ListAPIView):
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        category = self.kwargs['category']
        return Market.objects.filter(category=category)


def modify_marketInfo(request):
    table_data = JSONParser().parse(request)
    table = Market.objects.get(reg_num=table_data['reg_num'])
    serializer = MarketSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse("Update Successfully", safe=False)
    return JsonResponse("Failed to Update", safe=False)


def post_menu(request):
    requestedData = JSONParser().parse(request)
    serializer = PostSerializer(data=requestedData)
    if (serializer.is_valid()):
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    return JsonResponse("Failed to post new menu", safe=False, status=status.HTTP_400_BAD_REQUEST)


def delete_menu(request, regnum, uuid):
    if (Post.objects.filter(write_market=regnum, post_uuid=uuid).exists()):
        deletedData = Post.objects.get(write_market=regnum, post_uuid=uuid)
        deletedData.delete()
        return JsonResponse("Delete Successfully", safe=False)
    return JsonResponse("Failed to delete", safe=False)


def get_marketInfo_orderBy_distance(request, lat, lng, category):
    data = get_locations_nearby_coords(
        lat, lng, category)
    return JsonResponse(data, safe=False)


def get_locations_nearby_coords(latitude, longtitude, category, max_distance=None):
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longtitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longtitude, latitude)
    )
    qs = Market.objects.filter(category=category) \
        .annotate(distance=distance_raw_sql)\
        .order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance).values()
    return list(qs.values())


# 매장, 음식 같이 나오게 - 1

# review
# default 질문지 response : default 질문 목록 -Questionlist
# get/ get reviews by regNum: 매장별 리뷰 확인(reviewDate 이후 24시간 경과 리뷰만)
# post/ register question - Questionlist
# post/ fhinish choosing question - Quesbymarket
# post/ post review - Review
