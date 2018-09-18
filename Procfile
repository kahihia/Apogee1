web: bin/start-nginx daphne -u unix:///tmp/nginx.socket -v2 apogee1.asgi:application
celeryworker: celery -A apogee1.settings worker -l info
release: bash ./post_deploy.sh