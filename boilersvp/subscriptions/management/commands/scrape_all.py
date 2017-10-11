from django.core.management.base import BaseCommand

from ...tasks import scrape_all_events


class Command(BaseCommand):
    help = "Scrape all events at once."

    def handle(self, *args, **options):
        scrape_all_events()
