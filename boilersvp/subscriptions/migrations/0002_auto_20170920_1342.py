# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 13:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-start',)},
        ),
    ]
