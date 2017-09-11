web: cd boilersvp; python manage.py collectstatic --noinput; python manage.py migrate --noinput; waitress-serve --port=$PORT --threads=$WEB_CONCURRENCY boilersvp.wsgi:application
worker: python -u boilersvp/manage.py run_huey
