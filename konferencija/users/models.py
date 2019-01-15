#Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
#Local imports
from . import utils

#Custom user that has email instead as username field
class CustomUser(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    ulica = models.CharField(max_length = 20)
    kucni_broj = models.CharField(max_length = 20)
    grad = models.CharField(max_length = 20)
    drzava = models.CharField(max_length = 20)
    email_confirmed = models.BooleanField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name' ,'last_name']

    def __str__(self):
        list = self.email.split('@')
        return list[0] + '_' + str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.pk})



def post_save_reciever(sender,instance,*args,**kwargs):
    if instance.email_confirmed == 0:
        utils.send_mail_to(instance)
    else:
        print('logged in')

models.signals.post_save.connect(post_save_reciever,sender=CustomUser)
