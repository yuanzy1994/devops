from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32,null=True)
    password = models.CharField(max_length=32,null=True)
    age = models.CharField(max_length=3,null=True)