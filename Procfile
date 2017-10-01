web: cd boilersvp; python manage.py collectstatic --noinput; python manage.py migrate --noinput; waitress-serve --port=$PORT boilersvp.wsgi:application
worker: python -u boilersvp/manage.py run_huey
