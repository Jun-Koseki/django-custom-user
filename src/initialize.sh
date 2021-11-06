#!/bin/bash

sleep 10
export DJANGO_SETTINGS_MODULE=config.settings

python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin@example.com', 'p@ssw0rd', username='admin');"

python3 manage.py runserver 0.0.0.0:8000