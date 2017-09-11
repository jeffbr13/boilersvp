import logging

import requests
from dateutil.parser import parse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task, db_periodic_task, db_task

from .models import City, Event


logger = logging.getLogger(__name__)


@periodic_task(crontab(minute='*/5'))
def say_hello():
    logger.info('Hello!')


@db_periodic_task(crontab(minute='0'))
def fetch_all_events():
    next_url = 'https://archive.boilerroom.tv/api/shows/'
    while next_url:
        logger.info('Fetching <%s>…', next_url)
        resp = requests.get(next_url).json()
        next_url = resp['next']

        for event_json in resp['results']:
            logger.debug('Creating event from %s…', event_json)
            try:
                if event_json['city']:
                    city, created = City.objects.update_or_create(
                        url=event_json['city']['url'],
                        name=event_json['city']['name'],
                    )
                    logger.info('Created %r.' if created else 'Updated %r.', city)
                else:
                    city = None

                event_web_url = requests.get(
                    'https://boilerroom.tv/',
                    {'p': event_json['wordpress_id']},
                    allow_redirects=False,
                ).next.url

                event, created = Event.objects.update_or_create(
                    url=event_json['url'],
                    web_url=event_web_url,
                    name=event_json['title'],
                    city=city,
                    start=parse(event_json['start']),
                )
                logger.info('Created %r.' if created else 'Updated %r.', event)
                if created and event.start > timezone.now():
                    notify_subscribers(event.id)
            except:
                logger.exception('Could not create event from %s.', event_json)


@db_task()
def notify_subscribers(event_id):
    event = Event.objects.get(id=event_id)
    emails = []
    for subscriber in event.city.subscriber_set.all():
        emails.append((
            'Upcoming Boiler Room in %s: %s' % (event.city, event.name),
            'RSVP to %s at <%s>.' % (event.name, event.web_url),
            settings.DEFAULT_FROM_MAIL,
            (subscriber.email,),
        ))
    send_mass_mail(emails)
