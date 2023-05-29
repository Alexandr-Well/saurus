import random
from django.db import models



class Location(models.Model):
    zip = models.IntegerField(primary_key=True, db_index=True, unique=True)
    city = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ['zip']


class Car(models.Model):
    """
    для большей оптимизации можно сделать так:
    # number_digit = models.SmallIntegerField(max_length=4)
    # number_char = models.CharField(max_length=1)
    """
    number = models.CharField(max_length=5, unique=True, primary_key=True, db_index=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    capacity = models.SmallIntegerField()

    class Meta:
        ordering = ['number']

    def save(self, *args, **kwargs):
        # не самое лучшее решение
        if not self.location:
            indexes = tuple(map(lambda item: item.zip, Location.objects.only('zip').all()))
            self.location = Location.objects.get(zip=random.choice(indexes))
        super().save(*args, **kwargs)


class Cargo(models.Model):
    location_pickup = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location_from')
    location_delivery = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='location_to')
    weight = models.SmallIntegerField()
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ['-id']





