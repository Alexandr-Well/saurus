from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from django.db.models.query import QuerySet
from .models import Location, Cargo, Car
from .serializers import LocationSerializer, CargoSerializer, CarSerializer, CarSerializerCreate, \
    CargoWithCarsSerializer, CargoWithCarsListSerializer
from .utils.distance import DistanceCounter


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LocationApiSet(viewsets.ModelViewSet):
    """
        CRUD По всем Локациям
    """
    pagination_class = CommonPagination
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CarApiCreate(mixins.CreateModelMixin, GenericViewSet):
    """
        Создание Автомобиля с рандомной локацией
    """
    pagination_class = CommonPagination
    queryset = Car.objects.all()
    serializer_class = CarSerializerCreate


class CarApiSet(viewsets.ModelViewSet):
    """
        CRUD По всем Автомобилям
    """
    pagination_class = CommonPagination
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CargoApiSet(viewsets.ModelViewSet):
    """
        CRUD По всем Грузам
    """
    pagination_class = CommonPagination
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def get_object(self):
        if self.request.method == 'GET':
            obj = Cargo.objects.select_related('location_pickup').get(pk=self.kwargs.get('pk'))
            cars_list = list(map(lambda car: {
                car.number: DistanceCounter.count_distance(
                    (obj.location_pickup.lat, obj.location_pickup.lng),
                    (car.location.lat, car.location.lng))}, Car.objects.select_related('location').all()))
            obj.nearest_car = cars_list
            self.serializer_class = CargoWithCarsListSerializer
            return obj
        return super().get_object()

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            if self.request.method == 'GET' and not self.kwargs.get('pk'):
                try:
                    queryset = queryset.select_related('location_pickup').all()
                    for cargo in queryset:
                        cars_lte_450 = len(tuple(filter(lambda car:
                                                        DistanceCounter.count_distance(
                                                            fst_point=(float(cargo.location_pickup.lat),
                                                                       float(cargo.location_pickup.lng)),
                                                            dst_point=(
                                                            float(car.location.lat), float(car.location.lng))) <= 450,
                                                        tuple(Car.objects.select_related('location').all()))))
                        cargo.nearest_car = cars_lte_450
                    self.serializer_class = CargoWithCarsSerializer
                except AttributeError:
                    queryset = queryset.all()
            else:
                queryset = queryset.all()
        return queryset
