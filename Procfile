release: bash ./post_deploy.sh

web: bin/start-nginx gunicorn -c gunicorn.conf apogee1.wsgi:application daphne -p $PORT -b unix:/tmp/nginx_daphne.socket apogee1.asgi:application
celeryworker: celery -A apogee1.settings worker -l info
