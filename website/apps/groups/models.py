from django.db import models
from django.db.models import Model
from django.contrib.auth import get_user_model

from website.apps.servers.models import Server

class Group(Model):

    group = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

BAN_TYPES = (
    ('group', 'GROUP'),
    ('email', 'EMAIL'),
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
    ('certify', 'CERTIFY'),
    ('config', 'CONFIG')
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
    email  = models.CharField(max_length=64, default='')
    value  = models.CharField(max_length=64, default='')
    author = models.BigIntegerField()
