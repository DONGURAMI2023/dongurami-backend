from django.db import models

from accounts.models import User

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    building = models.IntegerField(default=0)
