from django.db import models
from django.db.models import Model

class Member(Model):

    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, default='')
    login = models.CharField(max_length=128)
