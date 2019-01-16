from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save,post_save
from django.urls import reverse

def clearString(str):
    str = ''.join(e for e in str if e.isalnum()).lower().replace('š','s').replace('ć','c').replace('č','c').replace('đ','d').replace('ž','z')
    return str

#Konferencija
class Konferencija(models.Model):
    creator = models.ForeignKey(CustomUser,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    chairman = models.ForeignKey(CustomUser,related_name='related_secondary_manual_roats', on_delete=models.CASCADE, default = creator)
    name = models.CharField(max_length=100, unique = True)
    description = models.CharField(max_length=4000)
    summary = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    sekcije = models.CharField(max_length=120)
    form = models.CharField(max_length = 1000, default = None)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="default.jpg")
    REQUIRED_FIELDS = ['creator','chairman','name']
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('conference:detail', kwargs={'pk': self.pk})

class Sekcija(models.Model):
    konferencija = models.ForeignKey(Konferencija, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.konferencija.name + '_' + self.name

    def get_absolute_url(self):
        return reverse('conference:sekcija', kwargs={'pk': self.pk})

class User_Sekcija(models.Model):
    sekcija = models.ForeignKey(Sekcija, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recenzent_not_approved = models.BooleanField(default=False)
    recenzent_approved =  models.BooleanField(default=False)
    questions = models.CharField(max_length = 1000, default = None)
    class Meta:
        unique_together = ("sekcija", "user")
    def __str__(self):
        return (self.user.email.split('@')[0] + '_' + self.sekcija.konferencija.name + '_' + self.sekcija.name).lower()

def user_directory_path(instance,filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    user_sekcija = ''.join(e for e in instance.user_sekcija.__str__() if e.isalnum())
    filename = ''.join(e for e in filename if e.isalnum())
    string = 'uploads/{0}/user_{1}/{2}'.format(clearString(instance.user_sekcija.__str__()),instance.user_sekcija.user.id,clearString(filename))
    return string

class Radovi(models.Model):
    user_sekcija = models.ForeignKey(User_Sekcija, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=user_directory_path)
    authors = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    approved = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user_sekcija.__str__() + '_' + self.title
    def get_absolute_url(self):
        return reverse('conference:radovi_detail', kwargs={'pk': self.pk})

def post_save_reciever(sender,instance,*args,**kwargs):
    for i in instance.sekcije.split(','):
        sekcija = Sekcija.objects.create(konferencija = instance, name = i)
        sekcija.save()

post_save.connect(post_save_reciever,sender=Konferencija)
