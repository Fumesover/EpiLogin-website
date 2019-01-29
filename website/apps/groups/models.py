from django.db import models
from django.db.models import Model

from website.apps.servers.models import Server

class Group(Model):

    group = models.CharField(max_length=128)
    login = models.CharField(max_length=128)

BAN_TYPES = (
    ('group', 'GROUP'),
    ('login', 'LOGIN'),
    ('user', 'USER'),
)

class Ban(Model):

    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        null=True
    )
    type   = models.CharField(
        choices=BAN_TYPES,
        max_length=64
    )
    value  = models.CharField(max_length=64, default='')

UPDATE_TYPES = (
    ('unban', 'UNBAN'),
    ('ban', 'BAN'),
    ('addgroup', 'ADDGROUP'),
    ('delgroup', 'DELGROUP'),
)

class Update(Model):

    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        null=True
    )
    type = models.CharField(
        choices=UPDATE_TYPES,
        max_length=20
    )
    ban_type = models.CharField(
        choices=BAN_TYPES,
        max_length=20
    )
    login = models.CharField(max_length=64, default='')
    value = models.CharField(max_length=64, default='')
