import json
import logging

import pytz
import requests
from dateutil.parser import parse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task, db_periodic_task, db_task
from lxml import html

from .models import City, Event


logger = logging.getLogger(__name__)


@periodic_task(crontab(minute='*/5'))
def say_hello():
    logger.info('Hello!')


@db_periodic_task(crontab(minute='0,15,30,45'))
def scrape_cities():
    logger.info('Scraping cities…')
    session = requests.session()
    next_url = 'https://archive.boilerroom.tv/api/cities/'
    while next_url:
        resp = session.get(next_url).json()
        for city_json in resp['results']:
            logger.debug('Updating/creating city from <%s>…', city_json['url'])
            city, created = City.objects.update_or_create(
                url=city_json['url'],
                name=city_json['name'],
            )
            logger.debug('Created %r.' if created else 'Updated %r.', city)
        next_url = resp['next']
    logger.info('Scraped cities.')


@db_periodic_task(crontab(minute='5,20,35,50'))
def scrape_upcoming_events():
    logger.info('Scraping upcoming events…')
    page = html.fromstring(requests.get('https://boilerroom.tv/upcoming/').content)
    content = json.loads(page.xpath('.//script[@id="content"]')[0].text)
    for event_json in content['sessions']:
        try:
            logger.debug('Updating/creating event from %s…', event_json['url'])
            city = City.objects.get(name=event_json['city'])
            event, created = Event.objects.update_or_create(
                url=event_json['url'],
                name=event_json['title'],
                city=city,
                defaults=dict(
                    start=parse(event_json['startTime']).astimezone(pytz.UTC),
                    end=parse(event_json['endTime']).astimezone(pytz.UTC),
                    can_rsvp=True if event_json['inviteList'] else False,
                ),
            )
            logger.info('Created %r.' if created else 'Updated %r.', event)
            if created and event.start > timezone.now():
                notify_subscribers(event.id)
        except:
            logger.exception('Could not create event from %s.', event_json)
    logger.info('Scraped all events.')


@db_task()
def notify_subscribers(event_id):
    event = Event.objects.get(id=event_id)
    logger.info('Notifying subscribers for %r…', event)
    emails = []
    for subscriber in event.city.subscriber_set.all():
        emails.append((
            'Upcoming Boiler Room in %s: %s' % (event.city, event.name),
            'You can %s "%s" at %s here:\n\n<%s>.' % (
                ('request an invitation to' if event.can_rsvp else 'watch'),
                event.name,
                event.start,
                event.url,
            ),
            settings.DEFAULT_FROM_EMAIL,
            (subscriber.email,),
        ))
    send_mass_mail(emails)
    logger.info('Sent emails to %s subscribers for %r.', event.city.subscriber_set.count(), event)
