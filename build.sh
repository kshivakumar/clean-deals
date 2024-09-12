#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_sample_data --run-only-if-no-users