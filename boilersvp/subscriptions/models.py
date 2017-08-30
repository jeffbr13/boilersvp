from django.db import models


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=300)
    start = models.DateTimeField()

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField()
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.email
