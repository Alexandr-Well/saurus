from django.contrib import admin
from .models import Location, Car, Cargo


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass
