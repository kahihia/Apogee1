python manage.py migrate event_payment zero
python manage.py migrate account zero
python manage.py migrate parties zero
python manage.py migrate userstatistics zero
python manage.py migrate bids zero
python manage.py migrate notifications zero
python manage.py makemigrations --noinput
python manage.py migrate event_payment
python manage.py migrate auth --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
