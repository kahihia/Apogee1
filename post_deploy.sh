yes | python manage.py makemigrations parties
yes | python manage.py makemigrations event_payment
yes | python manage.py makemigrations
yes | python manage.py migrate --fake-initial
yes | python manage.py migrate parties
yes | python manage.py migrate event_payment
yes | python manage.py migrate auth
yes | python manage.py migrate
yes | python manage.py collectstatic