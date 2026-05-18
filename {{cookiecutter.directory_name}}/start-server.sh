#!/usr/bin/env bash
echo "Hello from {{ cookiecutter.project_title }}"
uv run manage.py collectstatic --no-input
echo "running migrations"
uv run manage.py migrate --no-input
uv run gunicorn dboeannotation.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 & nginx -g "daemon off;"