from dataclasses import field
from django.core import serializers
from rest_framework import serializers
from .models import NewTable, Customer, Quesbymarket, Questionlist, Review, Market, Post

# Serializer: 정의한 field만을 return


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewTable
        fields = '__all__'
        # uuid, email, name, age 값만 return 시키도록함.

# foodTesting Serializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class QuesbymarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quesbymarket
        fields = '__all__'


class QuestionlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionlist
        fields = '__all__'


'''
class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewTable
        fields=('email','name','nickname','gender','profile','born_date','type')
        
class StoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewTable
        fields=('사업자등록번호(수정필요)','restaurant_name','restaurant_photo','menu_list','menu_photo_list')
'''
