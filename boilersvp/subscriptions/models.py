from django.db import models


class City(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    url = models.URLField(unique=True)
    web_url = models.URLField(unique=True)
    name = models.CharField(max_length=300)
    city = models.ForeignKey(City, null=True, blank=True)
    start = models.DateTimeField()

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField()
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.email
