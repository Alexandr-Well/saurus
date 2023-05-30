from drf_yasg import openapi
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
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

    @staticmethod
    def get_cars_with_distance(cars, cargo):
        cars_list = tuple(map(lambda car:
                              DistanceCounter.count_distance(
                                  fst_point=(float(cargo.location_pickup.lat), float(cargo.location_pickup.lng)),
                                  dst_point=(float(car.location.lat), float(car.location.lng))),
                              cars))
        return cars_list

    def get_filtered_cars(self, cargo, cars_list, default):
        cargo.nearest_car = len(tuple(filter(
            lambda item: item <= self.get_manage_filtering().get('_nearest_car', default), cars_list
        )))

    def get_filtering(self):
        flt = {}
        for key, val in self.request.query_params.items():
            if key.startswith('_') or key.startswith('__'):
                continue
            flt[key] = val
        return flt

    def get_manage_filtering(self):
        flt = {}
        for key, val in self.request.query_params.items():
            if key.startswith('_'):
                flt[key] = val
        return flt

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('weight', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Filter: equal'),
            openapi.Parameter('weight__lte', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Filter: less then'),
            openapi.Parameter('weight__gte', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Filter: more then'),
            openapi.Parameter('_min_distance', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Filter: min_distance'),
            openapi.Parameter('_nearest_car', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Filter: count car near by input value, default 450'),
        ])
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_object(self):
        if self.request.method == 'GET':
            obj = Cargo.objects.select_related('location_pickup').get(pk=self.kwargs.get('pk'))
            cars_list = list(map(lambda car: {
                car.number: DistanceCounter.count_distance((obj.location_pickup.lat, obj.location_pickup.lng),
                                                           (car.location.lat, car.location.lng))},
                                 Car.objects.select_related('location').all()))
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
                queryset = queryset.select_related('location_pickup').filter(**self.get_filtering())
                cars = tuple(Car.objects.select_related('location').all())
                if self.get_manage_filtering().get('_min_distance'):
                    min_distance = self.get_manage_filtering().get('_min_distance')
                    to_exclude = []
                    qs = list(queryset)
                    for index, cargo in enumerate(qs):
                        cars_list = self.get_cars_with_distance(cars, cargo)
                        self.get_filtered_cars(cargo, cars_list, 450)
                        if min_distance < min(cars_list):
                            to_exclude.append(cargo)
                    if to_exclude:
                        for item in to_exclude:
                            qs.remove(item)
                        queryset = qs
                    else:
                        queryset = queryset
                else:
                    for cargo in queryset:
                        cars_list = self.get_cars_with_distance(cars, cargo)
                        self.get_filtered_cars(cargo, cars_list, 450)
                self.serializer_class = CargoWithCarsSerializer
            else:
                queryset = queryset.all()
        return queryset
