from django.http import HttpRequest
from django.shortcuts import render

from .forms import SubscriberForm


def index(request: HttpRequest):
    form = SubscriberForm(request.POST) if request.POST else SubscriberForm()

    return render(request, 'index.html', context={
        'form': form,
    })
