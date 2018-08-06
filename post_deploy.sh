python manage.py makemigrations --noinput
python manage.py migrate event_payment
python manage.py migrate auth --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
