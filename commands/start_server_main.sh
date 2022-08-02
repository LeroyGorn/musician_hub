#!/bin/bash

echo "Hello from mushub docker"
python src/manage.py migrate --settings=config.settings.${MODE}
python src/manage.py collectstatic --noinput --settings=config.settings.${MODE}

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./src config.wsgi:application --log-level=${WSGI_LOG_LEVEL}
