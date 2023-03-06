#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database makemigrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Apply database static"
python manage.py collectstatic --noinput


echo "Create admin"
python manage.py createsuperuser --email=$DJANGO_SUPERUSER_EMAIL --noinput || echo "admin already created"

echo "start server"
gunicorn wsgi --bind 0.0.0.0:8000 --workers=3 --timeout=120


exec "$@"

