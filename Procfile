web: gunicorn config.wsgi  --log-file -
worker: celery worker --app config.celeryconf -l info -E
release: python manage.py migrate
