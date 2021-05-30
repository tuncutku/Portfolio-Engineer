web: uwsgi uwsgi.ini
worker: celery -A run_celery.celery worker --loglevel=info
beat: celery -A run_celery.celery beat --loglevel=info