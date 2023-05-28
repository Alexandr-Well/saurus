from django.urls import path, include
from .api import LocationApiSet, CarApiSet, CargoApiSet, CarApiCreate
from rest_framework import routers

location = routers.DefaultRouter()
car = routers.DefaultRouter()
cargo = routers.DefaultRouter()

location.register(r'location', LocationApiSet)
car.register(r'car', CarApiSet, CarApiCreate)
cargo.register(r'cargo', CargoApiSet)

urlpatterns = [
    path('', include(location.urls)),
    path('', include(car.urls)),
    path('', include(cargo.urls)),
    path('car-random-logation/', CarApiCreate.as_view({'post': 'create'})),
]
