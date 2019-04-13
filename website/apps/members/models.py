from django.db import models
from django.db.models import Model
import random, string

from website.apps.servers.models import Server

def generate_hash():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))

class Member(Model):

    id       = models.BigIntegerField(primary_key=True)
    name     = models.CharField(max_length=128, blank=True)
    hash     = models.CharField(max_length=128, default=generate_hash, blank=True)
    email    = models.CharField(max_length=128, blank=True)
    servers  = models.ManyToManyField(Server, blank=True)
