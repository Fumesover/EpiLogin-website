from django.db import models
from django.db.models import Model
from django.contrib.postgres.fields import ArrayField

class Server(Model):

    id              = models.BigIntegerField(primary_key=True)
    channel_logs    = models.BigIntegerField(default=0)
    channel_admin   = models.BigIntegerField(default=0)
    channel_request = models.BigIntegerField(default=0)


RANK_TYPES = (
    ('classic', 'CLASSIC'),
    ('rank_confirmed', 'RANK_CONFIRMED'),
    ('rank_banned', 'RANK_BANNED'),
)

class Rank(Model):

    server     = models.ForeignKey(Server, on_delete=models.CASCADE)
    type       = models.CharField(choices=RANK_TYPES, max_length=16)
    name       = models.CharField(max_length=64)
    discord_id = models.BigIntegerField()
