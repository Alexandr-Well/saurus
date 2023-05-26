from rest_framework import viewsets
from .models import TestModel
from .serializers import WomenSerializer


class TestApiSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = WomenSerializer