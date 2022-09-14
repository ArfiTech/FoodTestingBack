from dataclasses import field
from django.core import serializers
from rest_framework import serializers
from .models import Customer
from .models import Market
from .models import Post
from .models import Review

# Serializer: 정의한 field만을 return


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함


class PostSerializer(serializers.ModelSerializer):
    class Meta :
        model = Post        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review        # product 모델 사용
        fields = '__all__'            # 모든 필드 포함
