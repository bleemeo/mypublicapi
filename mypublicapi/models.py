# -*- coding: utf-8 -*-

import uuid

from django.db import models


class Server(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        permissions = (
            ('view_server', 'Can view Server'),
        )

    def __unicode__(self):
        return self.name


class Metric(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    server = models.ForeignKey(Server)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        permissions = (
            ('view_metric', 'Can view Metric'),
        )

    def __unicode__(self):
        return self.name


class ServerProperty(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    server = models.ForeignKey(Server)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        permissions = (
            ('view_serverproperty', 'Can view Server Property'),
        )

    def __unicode__(self):
        return self.name

