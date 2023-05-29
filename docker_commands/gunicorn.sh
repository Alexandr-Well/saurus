#!/bin/bash

export DJANGO_SETTINGS_MODULE=settings.settings

python manage.py migrate

cd core/utils

python database_load_data.py

python schedule_script.py > /dev/null &

cd ../../


#python manage.py loaddata fixtures/location.json > /dev/null

#exec gunicorn settings.wsgi:application \
#    --name delivery_test \
#    --bind 0.0.0.0:8000 \
#    --workers 3 \
#    --log-level=info \
#    --log-file=/app/app_logs/gunicorn.log \
#    --access-logfile=/app/app_logs/gunicorn-access.log \
#    --error-logfile=/app/app_logs/gunicorn-error.log \
#"$@"

exec python manage.py runserver 0.0.0.0:8000