from django.db import models


class City(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Event(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=300)
    city = models.ForeignKey(City, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return '%s (%s)' % (self.name, self.start.strftime('%c'))


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.email
