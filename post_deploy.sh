yes | python manage.py makemigrations
yes | python manage.py migrate
python manage.py collectstatic --noinput
