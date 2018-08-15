release: bash ./post_deploy.sh

web: daphne -p $PORT -b 0.0.0.0 apogee1.asgi:application
worker: celery worker --app=parties.tasks
celeryworker: celery -A apogee1.settings worker -l info
