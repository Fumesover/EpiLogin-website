from django.db import models
from django.db.models import Model
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

class EmailDomain(Model):

    domain = models.CharField(max_length=64)

class Server(Model):

    id              = models.BigIntegerField(primary_key=True)
    is_active       = models.BooleanField(default=False)
    channel_logs    = models.BigIntegerField(default=0)
    channel_admin   = models.BigIntegerField(default=0)
    channel_request = models.BigIntegerField(default=0)
    admins          = models.ManyToManyField(get_user_model(), blank=True, related_name='admin')
    moderators      = models.ManyToManyField(get_user_model(), blank=True, related_name='moderator')
    emails_domains  = models.ManyToManyField(EmailDomain, blank=True)

RANK_TYPES = (
    ('classic', 'CLASSIC'),
    ('confirmed', 'CONFIRMED'),
    ('banned', 'BANNED'),
)

class Rank(Model):

    server     = models.ForeignKey(Server, on_delete=models.CASCADE)
    type       = models.CharField(choices=RANK_TYPES, max_length=16)
    name       = models.CharField(max_length=64, blank=True)
    discord_id = models.BigIntegerField()
