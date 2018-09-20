release: bash ./post_deploy.sh
web: bin/start-nginx gunicorn apogee1.asgi -c gunicorn.conf -k uvicorn.workers.UvicornWorker
celeryworker: celery -A apogee1.settings worker -l info
