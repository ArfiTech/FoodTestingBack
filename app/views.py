from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import Customer
from rest_framework.views import APIView
from .serializers import CustomerSerializer


class DataListAPI(APIView):
    def get(self, request):
        queryset = Customer.objects.all()
        print(queryset)
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)
