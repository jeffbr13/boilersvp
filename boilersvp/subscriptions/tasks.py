import logging

import requests
from dateutil.parser import parse
from huey import crontab
from huey.contrib.djhuey import periodic_task, db_periodic_task, db_task

from .models import City, Event

logger = logging.getLogger(__name__)


@periodic_task(crontab(minute='*/5'))
def say_hello():
    logger.info('Hello!')


@db_periodic_task(crontab(hour='*'))
def fetch_all_events():
    next_url = 'https://archive.boilerroom.tv/api/shows/'
    while next_url:
        logger.info('Fetching <%s>…', next_url)
        resp = requests.get(next_url).json()
        next_url = resp['next']

        for event_json in resp['results']:
            if event_json['city']:
                city, created = City.objects.update_or_create(
                    url=event_json['city']['url'],
                    name=event_json['city']['name'],
                )
                logger.info('Created %r.' if created else 'Updated %r.', city)
            else:
                city = None

            event, created = Event.objects.update_or_create(
                url=event_json['url'],
                name=event_json['title'],
                city=city ,
                start=parse(event_json['start']),
            )
            logger.info('Created %r.' if created else 'Updated %r.', event)
