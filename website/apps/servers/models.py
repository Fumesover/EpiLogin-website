from django.db import models
from django.db.models import Model

from website.apps.members.models import Member

class Server(Model):

    name = models.CharField(max_length=254)
    server_id = models.BigIntegerField()
    members = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return self.name
