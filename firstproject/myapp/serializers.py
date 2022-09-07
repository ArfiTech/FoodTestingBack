from dataclasses import field
from django.core import serializers
from rest_framework import serializers
from .models import NewTable

# Serializer: 정의한 field만을 return


class TableSerializer(serializers.ModelSerializer):
    uuid = serializers.IntegerField()

    class Meta:
        model = NewTable
        fields = ('uuid', 'email', 'name', 'age')
        # uuid, email, name, age 값만 return 시키도록함.
