import random

import django

django.setup()
import json
from core.models import Location, Car

data = Location.objects.first()

if not data:
    with open('../../fixtures/location.json') as file:
        data_to_db = json.load(file)

    to_sql = []
    for item in data_to_db:
        to_sql.append(Location(
            zip=item['pk'],
            city=item['fields']['city'],
            state_name=item['fields']['state_name'],
            lat=item['fields']['lat'],
            lng=item['fields']['lng'],
        ))
    Location.objects.bulk_create(to_sql)

data = Car.objects.first()



if not data:
    with open('../../fixtures/car.json') as file:
        data_to_db = json.load(file)
    indexes = tuple(map(lambda loc: loc.zip, Location.objects.only('zip').all()))
    to_sql = []
    for item in data_to_db:
        to_sql.append(Car(
            number=item['pk'],
            capacity=item['fields']['capacity'],
            location=Location.objects.get(zip=random.choice(indexes))
        ))
    Car.objects.bulk_create(to_sql)
