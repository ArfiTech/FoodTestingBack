from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer

from rest_framework.response import Response
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer


class ProductListAPI(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


def index(request):
    # return HttpResponse("안녕하세요 product에 오신것을 환영합니다.")
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'product/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'product/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    return redirect('product:detail', question_id=question.id)