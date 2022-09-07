from rest_framework.pagination import PageNumberPagination

# page size를 지정할 수 있음.


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5