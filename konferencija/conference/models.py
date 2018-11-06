from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save,post_save
from django.urls import reverse

#Konferencija
class conference(models.Model):
    creator = models.ForeignKey(CustomUser,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    chairman = models.ForeignKey(CustomUser,related_name='related_secondary_manual_roats', on_delete=models.CASCADE, default = creator)
    name = models.CharField(max_length=100, unique = True)
    created = models.DateTimeField(auto_now_add=True)
    sekcije = models.CharField(max_length=120)
    REQUIRED_FIELDS = ['creator','chairman','name']
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('conference:detail', kwargs={'pk': self.pk})


class Sekcija(models.Model):
    conferenceInstance = models.ForeignKey(conference, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique = True)
    def __str__(self):
        return self.conferenceInstance.name + ' ' + self.name

def post_save_reciever(sender,instance,*args,**kwargs):
    for i in instance.sekcije.split(','):
        sekcija = Sekcija.objects.create(conferenceInstance = instance, name = i)
        sekcija.save()

post_save.connect(post_save_reciever,sender=conference)
