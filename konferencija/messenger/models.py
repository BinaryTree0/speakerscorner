from django.db import models
from users.models import CustomUser

#Connection between two users
class Messenger(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sender')
    reciever = models.ForeignKey(CustomUser,on_delete= models.CASCADE,related_name='reciever')
    def __str__(self):
        return str(self.id)

#Messages model
class Messages(models.Model):
    messenger = models.ForeignKey(Messenger,on_delete=models.CASCADE)
    message = models.CharField(max_length = 1000)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.messenger)
