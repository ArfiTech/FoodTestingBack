from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Customer, Market, Post, Questionlist, Review
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import CustomerSerializer, MarketSerializer, PostSerializer, ReviewSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .pagination import MarketPagination, PostPageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import models
from django.db.models.expressions import RawSQL

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# foodTesting API

def login_user(request, email, pw):
    if (Customer.objects.filter(email=email).exists()):
        customer = Customer.objects.filter(email=email, password=pw)
        if (customer.exists()):
            return JsonResponse(list(customer.values()), safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse('Wrong password', safe=False, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse("Not exist email", safe=False, status=status.HTTP_404_NOT_FOUND)


def get_userinfo(request, uuid):
    if (Customer.objects.filter(uuid=uuid).exists()):
        data = list(Customer.objects.filter(uuid=uuid).values())[0]
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
        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)
    return JsonResponse("Failed to Update", safe=False, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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


@api_view(['POST'])
@csrf_exempt
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
    for data in marketInfo:
        data["market_photo"] = "http://ec2-13-125-198-213.ap-northeast-2.compute.amazonaws.com:8000/img/"+data['market_photo']
    postInfo = list(Post.objects.filter(write_market=regnum).values())
    for post in postInfo:
        post["menu_photo"] = "http://ec2-13-125-198-213.ap-northeast-2.compute.amazonaws.com:8000/img/"+post["menu_photo"]
    return JsonResponse({"market": marketInfo, "post": postInfo}, safe=False, status=status.HTTP_200_OK)


class getMarketInfobyUUID(ListAPIView):
    #queryset = Market.objects.all()
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        id = self.kwargs['uuid']
        marketInfo = list(Market.objects.filter(customer_uuid=id))
        for data in marketInfo:
            data["market_photo"] = "http://ec2-13-125-198-213.ap-northeast-2.compute.amazonaws.com:8000/img/"+data['market_photo']
        return JsonResponse(marketInfo, safe=False, status=status.HTTP_200_OK)


class getMarketInfobyCategory(ListAPIView):
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        category = self.kwargs['category']
        return Market.objects.filter(category=category)


@csrf_exempt
def modify_marketInfo(request):
    table_data = JSONParser().parse(request)
    table = Market.objects.get(reg_num=table_data['reg_num'])
    serializer = MarketSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse("Update Successfully", safe=False)
    return JsonResponse("Failed to Update", safe=False)


@api_view(['POST'])
@csrf_exempt
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
    for d in data:
        d["market_photo"] = "http://ec2-13-125-198-213.ap-northeast-2.compute.amazonaws.com:8000/img/"+d['market_photo']
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
    if (category == 'all'):
        qs = Market.objects.all()\
            .annotate(distance=distance_raw_sql)\
            .order_by('distance')
    else:
        qs = Market.objects.filter(category=category) \
            .annotate(distance=distance_raw_sql)\
            .order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance).values()
    return list(qs.values())


# 사장님이 선택한 질문 보내기


def getReviewQuestions(request, uuid):
    ques_uuid = list(Quesbymarket.objects.filter(
        market_reg_num=uuid).values('ques_uuid'))
    questions = []
    for uuid in ques_uuid:
        query_set = Questionlist.objects.filter(ques_uuid=uuid).values()
        questions.append(query_set)
    return JsonResponse(json.dumps(questions), safe=False, status=status.HTTP_200_OK)

# 사용자가 작성한 리뷰 post


@api_view(['POST'])
@csrf_exempt
def postReviews(request):
    requestedData = JSONParser().parse(request)
    review_uuid = requestedData['review_uuid']
    writer_uuid = requestedData['writer_uuid']
    market_reg_num = requestedData['market_reg_num']
    review_date = requestedData['review_date']
    answers = requestedData['answers']

    for answer in answers:
        ques = answer[0]
        ans = answer[1]
        review = {'review_uuid': review_uuid, 'writer_uuid': writer_uuid, 'market_reg_num': market_reg_num,
                  'ques_uuid': ques, 'review_line': ans, 'review_date': review_date}
        serializer = ReviewSerializer(data=json.dumps(review))
        if (serializer.is_valid()):
            serializer.save()
        else:
            return JsonResponse("Failed to register", safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse("Success to register", safe=False, status=status.HTTP_200_OK)

# 매장, 음식 같이 나오게 - 1

# review
# default 질문지 response : default 질문 목록 -Questionlist
# get/ get reviews by regNum: 매장별 리뷰 확인(reviewDate 이후 24시간 경과 리뷰만)
# post/ register question - Questionlist
# post/ fhinish choosing question - Quesbymarket
# post/ post review - Review
