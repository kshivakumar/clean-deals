#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --workers 3 --preload --bind 0.0.0.0:8000 --access-logfile - clean_deals.wsgi:application