import json

to_json = []
with open('uszips.csv') as file:

    for line in file.readlines():
        a = line.split(',')
        tmp = {"model": "core.location", "pk": int(a[0][1:-1]), "fields": {"city": a[3][1:-1], "state_name": a[5][1:-1], "lat": a[1][1:-1], "lng": a[2][1:-1]}}
        to_json.append(tmp)

to_file = json.dumps(to_json)

with open('../fixtures/location.json', 'w') as file:
    file.write(to_file)
