release: bash ./post_deploy.sh

web: bin/start-nginx gunicorn -c gunicorn.conf apogee1.wsgi:application
celeryworker: celery -A apogee1.settings worker -l info
