from django.db import models
from users.models import CustomUser

class Konferencija(models.Model):
    REQUIRED_FIELDS = ['name']
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
