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
        return JsonResponse({"MESSAGE": "Success to register"}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to register"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def modify_marketInfo(request):
    table_data = JSONParser().parse(request)
    table = Market.objects.get(reg_num=table_data['reg_num'])
    serializer = MarketSerializer(table, data=table_data)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse({"MESSAGE": "Success to modify"}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to Update"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def post_menu(request):
    requestedData = JSONParser().parse(request)
    serializer = PostSerializer(data=requestedData)
    if (serializer.is_valid()):
        serializer.save()
        return JsonResponse({"MESSAGE": "Success to post new menu"}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to post new menu"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def modify_menu(request):
    requestedData = JSONParser().parse(request)
    originData = Post.objects.get(
        write_market=requestedData["write_market"], post_uuid=requestedData['post_uuid'])
    serializers = PostSerializer(originData, data=requestedData)
    if (serializers.is_valid(raise_exception=True)):
        serializers.save()
        return JsonResponse({"MESSAGE": "Success to modify menu"}, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"MESSAGE": "Failed to modify menu"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


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
    if (len(data) > 30):
        data = data[:30]
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
        # 전체(all),한식(kf), 일식(jf), 중식(cf), 양식(wf), 디저트(de), 분식(sf), 기타(el)
        if (category == 'kf'):
            category = '한식'
        elif (category == 'jf'):
            category = '일식'
        elif (category == 'cf'):
            category = '중식'
        elif (category == 'wf'):
            category = '양식'
        elif (category == 'de'):
            category = '디저트'
        elif (category == 'sf'):
            category = '분식'
        else:
            category = '기타'
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
    ques_list = sorted(ques_list, key=lambda x: x["order"])
    questions = []
    for ques in ques_list:
        query_set = list(Questionlist.objects.filter(
            ques_uuid=ques['ques_uuid']).values())[0]
        print(query_set)
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
    requestedData = JSONParser().parse(request)["reviews"]
    to_deleted = Review.objects.filter(
        market_reg_num=requestedData[0]["market_reg_num"], writer_uuid=requestedData[0]["writer_uuid"])
    if (to_deleted.exists()):
        to_deleted.delete()
    for data in requestedData:
        review_uuid = data["review_uuid"]
        writer_uuid = data["writer_uuid"]
        market_reg_num = data["market_reg_num"]
        ques_uuid = data["ques_uuid"]
        review_date = data["review_date"]
        review_line = data["review_line"]

        review = {
            'review_uuid': review_uuid,
            'writer_uuid': writer_uuid,
            'market_reg_num': market_reg_num,
            'ques_uuid': ques_uuid,
            'review_line': review_line,
            'review_date': review_date
        }

        serializer = ReviewSerializer(data=review)
        if (serializer.is_valid()):
            serializer.save()
        else:
            return JsonResponse({"MESSAGE": "Failed to register"}, safe=False, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"MESSAGE": "Success to register"}, safe=False, status=status.HTTP_200_OK)


def getReviewAnswers(request, reg_num):
    # 사용자들이 작성한 리뷰 중 24시간 지난 리뷰만 return
    customers = list(Review.objects.filter(
        market_reg_num=reg_num).values('writer_uuid').distinct())
    review_all = []
    for customer in customers:
        review_by_customer = Review.objects.filter(
            market_reg_num=reg_num, writer_uuid=customer["writer_uuid"]).values()
        customer_data = Customer.objects.get(uuid=customer["writer_uuid"])
        customerInfo = {"email": customer_data.email, "gender": customer_data.gender, "nickname": customer_data.nickname, "age": str(int((time.localtime(time.time()).tm_year -
                        time.localtime(customer_data.born_date).tm_year+1)/10))+"0대"
                        }
        ques_and_ans = {"customer": customerInfo,
                        "market_reg_num": reg_num, "answer": []}
        for review in review_by_customer:
            if (Quesbymarket.objects.filter(ques_uuid=review["ques_uuid_id"]).exists()):
                question_content = Questionlist.objects.get(
                    ques_uuid=review["ques_uuid_id"]).contents
                review_date = review["review_date"]
                ques_and_ans["answer"].append(
                    {
                        "contents": question_content,
                        "review_line": review["review_line"],
                        "review_date": review_date,
                    }
                )
        if (ques_and_ans["answer"]):
            ques_and_ans["answer"] = sorted(
                ques_and_ans["answer"], key=lambda x: x["review_date"])
            review_all.append(ques_and_ans)
    return JsonResponse({"review_all": review_all}, json_dumps_params={'ensure_ascii': False}, safe=False, status=status.HTTP_200_OK)


@ csrf_exempt
def registerOverallQues(request):
    data = JSONParser().parse(request)["ques"]
    if (len(data) > 0):
        if (Quesbymarket.objects.filter(market_reg_num=data[0]["market_reg_num"]).exists()):
            Quesbymarket.objects.filter(
                market_reg_num=data[0]["market_reg_num"]).delete()
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
                "uuid": str(uuid.uuid4()),
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
    return JsonResponse({"MESSAGE": "No data"}, safe=False, status=status.HTTP_400_BAD_REQUEST)


# 리뷰 작성한 고객의 수, 성별, 나이대, 방문한 달
def getReviewResearch(request, regnum):
    customer_list = list(Review.objects.filter(market_reg_num=regnum).values(
        'writer_uuid', 'review_date').distinct())
    result = {
        "total": len(customer_list),
        "gender": {0: 0, 1: 0, 2: 0},
        "age": {10: 0, 20: 0, 30: 0, 40: 0, 50: 0},
        "per_month": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    }
    for customer in customer_list:
        gender = Customer.objects.get(uuid=customer['writer_uuid']).gender
        born_date = Customer.objects.get(
            uuid=customer['writer_uuid']).born_date
        review_date = customer['review_date']
        result["gender"][gender] += 1
        age = time.localtime(time.time()).tm_year - \
            time.localtime(born_date).tm_year+1
        if (age < 20):
            result["gender"][10] += 1
        elif (age < 30):
            result["gender"][20] += 1
        elif (age < 40):
            result["gender"][30] += 1
        elif (age < 50):
            result["gender"][40] += 1
        else:
            result["gender"][50] += 1
        month = time.localtime(review_date).tm_mon
        result["per_month"][month] += 1
    return JsonResponse({"review_result": result}, safe=False, status=status.HTTP_200_OK)


def getNewMarket(request, lat, lng):
    markets = sorted(get_locations_nearby_coords(
        lat, lng, 'all', max_distance=60), key=lambda market: market["start_date"], reverse=True)
    if (len(markets) > 15):
        markets = markets[:15]
    for market in markets:
        market["market_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/" + \
            market['market_photo']
        market['customer_uuid'] = market.pop('customer_uuid_id')
        del market["distance"]
    return JsonResponse({"markets": markets}, json_dumps_params={'ensure_ascii': False}, safe=False, status=status.HTTP_200_OK)


def getNewMenu(request):
    menus = list(Post.objects.all().order_by('-post_date').values())
    if (len(menus) > 15):
        menus = menus[:15]
    for menu in menus:
        menu["menu_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/" + \
            menu['menu_photo']
        menu['write_market'] = menu.pop('write_market_id')
        menu['writer_uuid'] = menu.pop('writer_uuid_id')
    return JsonResponse({"menus": menus}, json_dumps_params={'ensure_ascii': False}, safe=False, status=status.HTTP_200_OK)


def getCustomReview(request, uuid):
    review_all = list()
    visited_market = list(Review.objects.filter(
        writer_uuid=uuid).values('market_reg_num').distinct())
    for i in range(len(visited_market)):
        review_by_customer = list(Review.objects.filter(
            market_reg_num=visited_market[i]["market_reg_num"], writer_uuid=uuid).values())
        market_info = list(Market.objects.filter(
            reg_num=visited_market[i]["market_reg_num"]).values())[0]
        market_info["market_photo"] = "https://foodtesting-img.s3.ap-northeast-2.amazonaws.com/img/" + \
            market_info['market_photo']
        market_info["customer_uuid"] = market_info.pop('customer_uuid_id')
        ques_and_ans = {"customer": uuid,
                        "market_info": market_info, "answer": []}
        for review in review_by_customer:
            if (Quesbymarket.objects.filter(ques_uuid=review["ques_uuid_id"]).exists()):
                question_content = Questionlist.objects.get(
                    ques_uuid=review["ques_uuid_id"]).contents
                # question_order = Quesbymarket.objects.get(
                # market_reg_num=market["market_reg_num"], ques_uuid=review["ques_uuid"]).order
                review_date = review["review_date"]
                ques_and_ans["answer"].append(
                    {
                        "ques_uuid": review["ques_uuid_id"],
                        "review_uuid": review["review_uuid"],
                        "contents": question_content,
                        "review_line": review["review_line"],
                        "review_date": review_date,
                        # "order": question_order
                    }
                )
        if (ques_and_ans["answer"]):
            ques_and_ans["answer"] = sorted(
                ques_and_ans["answer"], key=lambda x: x["review_date"])
            review_all.append(ques_and_ans)
    return JsonResponse({"review_all": review_all}, json_dumps_params={'ensure_ascii': False}, safe=False, status=status.HTTP_200_OK)
