from msilib import Table
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.http.response import HttpResponse
from .serializers import CustomerSerializer, MarketSerializer, PostSerializer, ReviewSerializer, TableSerializer, QuesbymarketSerializer, QuestionlistSerializer
from myapp.models import NewTable, Customer, Market, Post, Questionlist, Review
from rest_framework.viewsets import ModelViewSet
from .models import NewTable, Quesbymarket
from .serializers import TableSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import MarketPagination, PostPageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import models
from django.db.models.expressions import RawSQL
from django.core import serializers
import json
import time
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def showData(request):
    data = list(NewTable.objects.values())
    return JsonResponse(data, safe=False)


# ListAPIView를 이용한 pagination/filter

class PostViewSet(ListAPIView):
    # queryset = NewTable.objects.all()
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
        # data = NewTable.objects.all()
        # serialized_data = TableSerializer(data, many=True)
        return HttpResponse("Not exists", status=404)

    elif request.method == 'POST':
        return HttpResponse('post')


@api_view(['POST'])
def post_api(request):
    if request.method == 'POST':
        requestedData = JSONParser().parse(request)["customer"]
        for customer in requestedData:
            serializer = TableSerializer(data=customer)
            if (serializer.is_valid()):
                serializer.save()
            else:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
        return Response("success", status=status.HTTP_201_CREATED)


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

def login_user(request, email, pw):
    if (Customer.objects.filter(email=email).exists()):
        customer = Customer.objects.filter(email=email, password=pw)
        if (customer.exists()):
            return JsonResponse(list(customer.values())[0], safe=False, status=status.HTTP_200_OK)
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
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    return JsonResponse("Failed to Update", safe=False, status=status.HTTP_400_BAD_REQUEST)


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
    if (len(marketInfo) > 0):
        for data in marketInfo:
            data["market_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/" + \
                data['market_photo']
            data['customer_uuid'] = data.pop('customer_uuid_id')
            postInfo = list(Post.objects.filter(write_market=regnum).values())
            for post in postInfo:
                post["menu_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/"+post["menu_photo"]
                post['write_market'] = post.pop('write_market_id')
                post['writer_uuid'] = post.pop('writer_uuid_id')
        return JsonResponse([{"market": marketInfo[0], "post": postInfo}], safe=False, status=status.HTTP_200_OK)
    else:
        JsonResponse({"MESSAGE": "Not exists store"}, safe=False,
                     status=status.HTTP_400_BAD_REQUEST)


def getMarketInfobyUUID(request, uuid):

    marketInfo = list(Market.objects.filter(customer_uuid=uuid).values())
    result = []
    for data in marketInfo:
        data["market_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/" + \
            data['market_photo']
        postInfo = list(Post.objects.filter(
            write_market=data["reg_num"]).values())
        for post in postInfo:
            post["menu_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/"+post["menu_photo"]
        result.append({"market": data, "post": postInfo})
    return JsonResponse(result, safe=False)


class getMarketInfobyCategory(ListAPIView):
    serializer_class = MarketSerializer
    pagination_class = MarketPagination

    def get_queryset(self):
        category = self.kwargs['category']
        return Market.objects.filter(category=category)


@csrf_exempt
def register_marketInfo(request):
    table_data = JSONParser().parse(request)
    if (Market.objects.filter(reg_num=table_data["reg_num"]).exists()):
        return JsonResponse({"MESSAGE": "already registered store"}, safe=False, status=status.HTTP_403_FORBIDDEN)
    serializer = MarketSerializer(data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to register"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def modify_marketInfo(request):
    table_data = JSONParser().parse(request)
    table = Market.objects.get(reg_num=table_data['reg_num'])
    serializer = MarketSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"MESSAGE": "Failed to Update"}, safe=False)


@csrf_exempt
def post_menu(request):
    requestedData = JSONParser().parse(request)
    serializer = PostSerializer(data=requestedData)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse({"MESSAGE": "Success to post new menu"}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to post new menu"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def delete_menu(request, regnum, uuid):
    if (Post.objects.filter(write_market=regnum, post_uuid=uuid).exists()):
        deletedData = Post.objects.get(write_market=regnum, post_uuid=uuid)
        deletedData.delete()
        return JsonResponse({"MESSAGE": "Delete Successfully"}, safe=False)
    return JsonResponse({"MESSAGE": "Failed to delete"}, safe=False)


def get_marketInfo_orderBy_distance(request, lat, lng, category):
    data = get_locations_nearby_coords(
        lat, lng, category)
    for d in data:
        d["market_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/"+d['market_photo']
        del d["distance"]
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


def getReviewQuestions(request, reg_num):
    # 사장님이 선택한 질문 보내기
    ques_list = list(Quesbymarket.objects.filter(
        market_reg_num=reg_num).values('ques_uuid', 'order'))
    ques_list = sorted(ques_list, lambda x: x["order"])
    questions = []
    for ques in ques_list:
        query_set = Questionlist.objects.filter(
            ques_uuid=ques('ques_uuid')).first()
        query_set["fast_response"] = query_set["fast_response"].split(",")
        query_set["order"] = ques["order"]
        questions.append(json.dumps(query_set))
    return JsonResponse({"ques": questions}, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
# 미사용 API
def registerQuestions(request):
    # 사장님이 선택한 질문들 post
    requestedData = JSONParser().parse(request)
    if (requestedData and Quesbymarket.objects.exists(market_reg_num=requestedData[0]["market_reg_num"])):
        return JsonResponse("already register questions", safe=False, status=status.HTTP_403_FORBIDDEN)
    for data in requestedData:
        question = {
            "market_reg_num": data["market_reg_num"],
            "ques_uuid": data["ques_uuid"],
            "order": data["order"]
        }
        serializer = QuesbymarketSerializer(data=question)
        if (serializer.is_valid()):
            serializer.save()
        else:
            return JsonResponse("Failed to register question", safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse("Success to register questions by market", safe=False, status=status.HTTP_200_OK)


@csrf_exempt
# 미사용 API
def postReviewQuestions(request):
    # 사장님이 작성한 질문 post
    requestedData = JSONParser().parse(request)["ques"]
    for data in requestedData:
        data["fast_response"] = list(
            map(lambda x: x.strip(), data["fast_response"]))
        data["fast_response"] = ",".join(data["fast_response"])
        serializer = QuestionlistSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse("Success to post", safe=False, status=status.HTTP_200_OK)
    return JsonResponse("Failed to post new menu", safe=False, status=status.HTTP_400_BAD_REQUEST)


def getDefaultQuestions(request, type):
    questions = list(Questionlist.objects(ques_type=type).values())
    for q in questions:
        q["fast_response"] = q["fast_response"].split(",")
        q["fast_response"] = list(map(lambda x: x.strip(), q["fast_response"]))
    return JsonResponse(questions, safe=False, status=status.HTTP_200_OK)


@ csrf_exempt
def postReviews(request):
    # 사용자가 작성한 리뷰 post
    requestedData = JSONParser().parse(request)
    for data in requestedData:
        review_uuid = data["uuid"]
        writer_uuid = data["writer_uuid"]
        market_reg_num = data["RestaurantRegNumber"]
        ques_uuid = data["query_uuid"]
        review_date = data["post_date"]
        review_line = data["contents"]

        review = {
            'review_uuid': review_uuid,
            'writer_uuid': writer_uuid,
            'market_reg_num': market_reg_num,
            'ques_uuid': ques_uuid,
            'review_line': review_line,
            'review_date': review_date
        }

        serializer = ReviewSerializer(data=json.dumps(review))
        if (serializer.is_valid()):
            serializer.save()
        else:
            return JsonResponse({"MESSAGE": "Failed to register"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"MESSAGE": "Success to register"}, safe=False, status=status.HTTP_200_OK)


def getReviewAnswers(request, reg_num):
    # 사용자들이 작성한 리뷰 중 24시간 지난 리뷰만 return
    customers = list(Review.objects.filter(
        market_reg_num=reg_num).values('writer_uuid'))
    customers = list(set(customers))
    review_all = []
    for customer in customers:
        review_by_customer = Review.objects.filter(
            market_reg_num=reg_num, writer_uuid=customer).values()
        ques_and_ans = {"customer": customer,
                        "market_reg_num": reg_num, "answer": []}
        for review in review_by_customer:
            question_content = Questionlist.objects.get(
                ques_uuid=review["ques_uuid"]).contents
            question_order = Quesbymarket.objects.get(
                market_reg_num=reg_num, ques_uuid=review["ques_uuid"]).order
            review_date = review["review_date"]
            if ((int(time.time())-review_date)/60*60*24 > 24):
                ques_and_ans["answer"].append(
                    {
                        "ques_uuid": review["ques_uuid"],
                        "ques_type": review["ques_type"],
                        "review_uuid": review["review_uuid"],
                        "contents": question_content,
                        "review_line": review["review_line"],
                        "review_date": review_date,
                        "order": question_order
                    }
                )
            if (ques_and_ans["answer"]):
                ques_and_ans = sorted(ques_and_ans, lambda x: x["order"])
                review_all.append(ques_and_ans)

    return JsonResponse(review_all, safe=False, status=status.HTTP_200_OK)


@ csrf_exempt
def registerOverallQues(request):
    data = JSONParser().parse(request)["ques"]
    if (len(data) > 0):
        if (Questionlist.objects.filter(market_reg_num=data[0]["market_reg_num"]).exists()):
            return JsonResponse({"MESSAGE": "already register overall questions"}, safe=False, status=status.HTTP_403_FORBIDDEN)
    for i in range(len(data)):
        if (data[i]["ques_type"] == 2):
            data[i]["fast_response"] = list(
                map(lambda x: x.strip(), data[i]["fast_response"]))
            data[i]["fast_response"] = ",".join(data[i]["fast_response"])
            question = {
                "ques_uuid": data[i]["ques_uuid"],
                "market_reg_num": data[i]["market_reg_num"],
                "contents": data[i]["contents"],
                "fast_response": data[i]["fast_response"],
                "ques_type": data[i]["ques_type"],
            }
            serializer = QuestionlistSerializer(data=question)
            print(repr(serializer))
            if (serializer.is_valid()):
                serializer.save()
            else:
                return JsonResponse({"MESSAGE": "Failed to register custom question"}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        selected_ques = {
            "market_reg_num": data[i]["market_reg_num"],
            "ques_uuid": data[i]["ques_uuid"],
            "order": i
        }
        selected_serializer = QuesbymarketSerializer(data=selected_ques)
        if (selected_serializer.is_valid()):
            selected_serializer.save()
        else:
            return JsonResponse({"MESSAGE": "Failed to register selected question"}, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
    return JsonResponse({"MESSAGE": "Success to register all selected questions"}, safe=False, status=status.HTTP_200_OK)


# 매장, 음식 같이 나오게 - 1

# review
# default 질문지 response : default 질문 목록 -Questionlist
# get/ get reviews by regNum: 매장별 리뷰 확인(reviewDate 이후 24시간 경과 리뷰만)
# post/ register question - Questionlist
# post/ fhinish choosing question - Quesbymarket
# post/ post review - Review
