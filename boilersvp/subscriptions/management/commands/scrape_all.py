from django.core.management.base import BaseCommand

from ...tasks import scrape_upcoming_events, scrape_cities


class Command(BaseCommand):
    help = "Scrape all events at once."

    def handle(self, *args, **options):
        scrape_cities()
        scrape_upcoming_events()
