from django.db import models
from django.db.models import Model

class Group(Model):

    group = models.CharField(max_length=128)
    login = models.CharField(max_length=128)
