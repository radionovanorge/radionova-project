#!/bin/sh
set -eu
export DJANGO_SETTINGS_MODULE=radionova.test_settings
python manage.py migrate --noinput
exec gunicorn --bind 0.0.0.0:8000 --access-logfile - --error-logfile - --capture-output radionova.diagnostic_wsgi:application
