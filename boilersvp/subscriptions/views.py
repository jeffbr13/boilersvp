from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render

from .forms import SubscriberForm


def index(request: HttpRequest):

    if request.POST:
        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You've subscribed!")

    else:
        form = SubscriberForm()

    return render(request, 'index.html', context={
        'form': form,
    })
