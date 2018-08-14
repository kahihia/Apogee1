release: bash ./post_deploy.sh

web: gunicorn apogee1.wsgi.py
web: daphne -p $PORT apogee1.asgi:application
worker: celery worker --app=parties.tasks
celeryworker: celery -A apogee1.settings worker -l info
