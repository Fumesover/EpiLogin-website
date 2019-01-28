from django.db import models
from django.db.models import Model

class Group(Model):

    group = models.CharField(max_length=128)
    login = models.CharField(max_length=128)

BAN_TYPES = (
    ('S', 'SERVER'),
    ('L', 'LOGIN'),
    ('U', 'USER'),
)

class Ban(Model):

    type = models.CharField(
        choices=BAN_TYPES,
        max_length=64
    )
    value = models.CharField(max_length=64, default='')
