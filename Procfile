web: gunicorn apogee1.wsgi.py
release: python manage.py makemigrations --noinput
release: python manage.py migrate auth --noinput
release: python manage.py migrate --noinput
release: python manage.py collectstatic --noinput
web: python manage.py runserver 0.0.0.0:$PORT
worker: celery worker --app=parties.tasks
celeryworker: celery -A apogee1.settings worker -l info