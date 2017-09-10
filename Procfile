web: cd boilersvp; python manage.py collectstatic --noinput; python manage.py migrate; python -u manage.py runserver 0.0.0.0:$PORT
worker: python -u boilersvp/manage.py run_huey
