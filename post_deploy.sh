python manage.py makemigrations --noinput
python manage.py migrate auth --noinput
python manage.py migrate --noinput

python manage.py collectstatic --noinput
