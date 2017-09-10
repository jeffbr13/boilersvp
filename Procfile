web: python boilersvp/manage.py collectstatic --noinput; python boilersvp/manage.py migrate; python -u boilersvp/manage.py runserver $PORT
worker: python -u boilersvp/manage.py run_huey
