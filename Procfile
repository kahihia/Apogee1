release: bash ./post_deploy.sh

web: gunicorn apogee1.wsgi
celeryworker: celery -A apogee1.settings worker -l info
