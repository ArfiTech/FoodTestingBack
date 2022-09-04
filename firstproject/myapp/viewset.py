from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import NewTable
from .serializers import TableSerializer
from .pagination import PostPageNumberPagination


class PostViewSet(ModelViewSet):
    queryset = NewTable.objects.all()
    serializer_class = TableSerializer
    pagination_class = PostPageNumberPagination
