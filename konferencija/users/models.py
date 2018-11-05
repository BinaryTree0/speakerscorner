from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save

class CustomUser(AbstractUser):
    recenzent = models.BooleanField(default=False)

    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


def pre_save_reciever(sender,instance,*args,**kwargs):
    print(instance.recenzent)

pre_save.connect(pre_save_reciever,sender=CustomUser)
