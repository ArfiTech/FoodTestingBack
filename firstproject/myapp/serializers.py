from dataclasses import field
from django.core import serializers
from rest_framework import serializers
from .models import NewTable


class TableSerializer(serializers.ModelSerializer):
    uuid = serializers.IntegerField()

    class Meta:
        model = NewTable
        fields = ('uuid', 'email', 'name', 'age')
