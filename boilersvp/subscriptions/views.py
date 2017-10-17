from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render
from django_ical.views import ICalFeed

from .models import Event
from .forms import SubscriberForm


def index(request: HttpRequest):

    if request.POST:
        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You've subscribed!")
        else:
            messages.error(request, form.errors)

    else:
        form = SubscriberForm()

    return render(request, 'index.html', context={
        'form': form,
    })


class AllEventsCalendarFeed(ICalFeed):
    product_id = '-//boilersvp.jeffbr13.net//All Events'
    title = 'Boiler Room Events'

    timezone = 'UTC'

    def items(self):
        return Event.objects.all().order_by('-start')

    def item_title(self, item):
        return item.name

    def item_start_datetime(self, item):
        return item.start

    def item_end_datetime(self, item):
        return item.end

    def item_location(self, item):
        return item.city.name if item.city else ''

    def item_link(self, item):
        return item.url
