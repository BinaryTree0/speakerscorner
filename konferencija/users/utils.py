from django import utils
from konferencija.settings import EMAIL_HOST
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site

def send_mail_to(instance):
    #Security mesures creation of custom token and uid
    token = default_token_generator.make_token(instance)
    uid = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(instance.pk))
    uid = uid.decode("utf-8")
    #Sending mail
    from_email = EMAIL_HOST
    current_site = Site.objects.get_current()
    current_site.domain
    message = 'http://' + current_site.domain  + '/users/validate/'+ uid + '/' + token +'/'
    send_mail('Registration',message,from_email,[instance.email],fail_silently=False,)
