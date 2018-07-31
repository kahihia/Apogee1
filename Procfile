release: python manage.py migrate --run-syncdb
release: python manage.py makemigrations
release: python manage.py migrate auth
release: python manage.py migrate
release: python manage.py collectstatic

web: gunicorn apogee1.wsgi.py
web: python manage.py runserver 0.0.0.0:$PORT
worker: celery worker --app=parties.tasks
celeryworker: celery -A apogee1.settings worker -l info