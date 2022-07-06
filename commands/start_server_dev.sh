#!/bin/bash

echo "Hello from mushub docker"
python src/manage.py migrate --settings=config.settings.${MODE}
python src/manage.py runserver --settings=config.settings.${MODE} 0:${WSGI_PORT}
