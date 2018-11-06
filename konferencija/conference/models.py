from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save

class conference(models.Model):
    creator = models.ForeignKey(CustomUser,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    chairman = models.ForeignKey(CustomUser,related_name='related_secondary_manual_roats', on_delete=models.CASCADE, default = creator)
    name = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['creator','chairman','name']
    def __str__(self):
        return self.name

def pre_save_reciever(sender,instance,*args,**kwargs):
    print('---------------')
    print(instance.chairman)

pre_save.connect(pre_save_reciever,sender=conference)
