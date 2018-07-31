web: gunicorn apogee1.wsgi.py
web: python manage.py runserver 0.0.0.0:$PORT
release: ./post_install.sh
worker: celery worker --app=parties.tasks
celeryworker: celery -A apogee1.settings worker -l info