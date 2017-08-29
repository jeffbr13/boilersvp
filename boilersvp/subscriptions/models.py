from django.db import models


class City(models.Model):
    name = models.CharField(max_length=200)


class Event(models.Model):
    name = models.CharField(max_length=300)
    start = models.DateTimeField()


class Subscriber(models.Model):
    email = models.EmailField()
    cities = models.ManyToManyField(City)
