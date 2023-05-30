import random
import time
import schedule
import django

django.setup()
from core.models import Car, Location


def job():
    try:
        loc = tuple(Location.objects.all())
        cars = Car.objects.all()
        for car in cars:
            car.location = random.choice(loc)
        Car.objects.bulk_update(cars, ['location'])
    except Exception as err:
        pass
        # with open('err.txt', 'w') as file:
        #     file.write(str(err))


schedule.every(180).seconds.do(job)

while True:
    time.sleep(60)
    schedule.run_pending()
