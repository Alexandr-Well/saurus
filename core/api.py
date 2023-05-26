from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import TestModel
from .serializers import WomenSerializer


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TestApiSet(viewsets.ModelViewSet):
    pagination_class = CommonPagination
    queryset = TestModel.objects.all()
    serializer_class = WomenSerializer