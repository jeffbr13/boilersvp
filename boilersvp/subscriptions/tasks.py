import logging

from huey import crontab
from huey.contrib.djhuey import periodic_task, db_periodic_task


@periodic_task(crontab(minute='*/5'))
def say_hello():
    print('Hello!')


@db_periodic_task(crontab(minute='*/5'))
def scrape_all_cities():
    from .models import City
    import requests

    resp = requests.get('https://archive.boilerroom.tv/api/cities/').json()
    cities = resp['results']

    while resp['next']:
        resp = requests.get(resp['next']).json()
        cities += resp['results']

    for city in cities:
        instance, created = City.objects.update_or_create(name=city['name'])
        logging.info('Created %r.' if created else 'Updated %r.', instance)
        print('Hello %r' % instance)


def scrape_all_events():
    from .models import Event
    import requests

    resp = requests.get('https://arhive.boilerroom.tv/api/shows/').json()
    events = resp['results']
    while resp['next']:
        resp = requests.get(resp['next']).json()
        events += resp['results']

    for event in events:
        instance, created = Event.objects.update_or_create(name=event['name'])
        logging.info('Created %r.' if created else 'Updated %r.', instance)
