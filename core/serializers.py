from rest_framework import serializers
from .models import Location, Cargo, Car


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CarSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('number', 'capacity')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cargo
        fields = "__all__"


class CargoWithCarsSerializer(CargoSerializer):
    location_pickup = LocationSerializer(many=False)
    location_delivery = LocationSerializer(many=False)
    nearest_car = serializers.IntegerField()


class CargoWithCarsListSerializer(CargoWithCarsSerializer):
    nearest_car = serializers.ListField(child=serializers.DictField())
