from rest_framework import serializers
from .models import Location, Cargo, Car
from .utils.validators import CarNumberValidator, WeightValidator


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CarSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('number', 'capacity')
        validators = [CarNumberValidator(field_name='number', mask='[0-9]{4}[A-Z]'),
                      WeightValidator(field_name='capacity', weight_min=1, weight_max=1000), ]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        validators = [CarNumberValidator(field_name='number', mask='[0-9]{4}[A-Z]'),
                      WeightValidator(field_name='capacity', weight_min=1, weight_max=1000), ]


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"
        validators = [WeightValidator(field_name='weight', weight_min=1, weight_max=1000), ]


class CargoWithCarsSerializer(CargoSerializer):
    location_pickup = LocationSerializer(many=False)
    location_delivery = LocationSerializer(many=False)
    nearest_car = serializers.IntegerField()


class CargoWithCarsListSerializer(CargoWithCarsSerializer):
    nearest_car = serializers.ListField(child=serializers.DictField())
