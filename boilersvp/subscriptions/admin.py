from django.contrib import admin

from .models import City, Event, Subscriber


admin.site.register(City)
admin.site.register(Event)
admin.site.register(Subscriber)
