from django.urls import path, include
from .api import TestApiSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'prefix', TestApiSet)

urlpatterns = [
    path('test/', include(router.urls)),
]