from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render

from .models import Customer, Market, Post
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import CustomerSerializer, MarketSerializer, ReviewSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .pagination import MarketPagination, PostPageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


# class DataListAPI(APIView):
#     def get(self, request):
#         queryset = Customer.objects.all()
#         print(queryset)
#         serializer = CustomerSerializer(queryset, many=True)
#         return Response(serializer.data)

def get_userinfo(request, uuid):
    if (Customer.objects.filter(uuid=uuid).exists()):
        data = list(Customer.objects.filter(uuid=uuid).values())
        # attribute -> serializer or all values()
        return JsonResponse(data, safe=False, status=200)
    return HttpResponse("Not exists", safe=False, status=404)


@csrf_exempt
def modify_userinfo(request):
    table_data = JSONParser().parse(request)
    table = Customer.objects.get(uuid=table_data['uuid'])
    serializer = CustomerSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse("Update Successfully", safe=False)
    return JsonResponse("Failed to Update", safe=False)


@csrf_exempt
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


class getMarketInfobyRegNum(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        regnum = self.kwargs['regnum']
        return Market.objects.filter(reg_num=regnum)


class getMarketInfobyUUID(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        id = self.kwargs['uuid']
        return Market.objects.filter(customer_uuid=id)


@csrf_exempt
def modify_marketInfo(request):
    table_data = JSONParser().parse(request)
    table = Market.objects.get(reg_num=table_data['reg_num'])
    serializer = MarketSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse("Update Successfully", safe=False)
    return JsonResponse("Failed to Update", safe=False)