#View imports
from django.views import generic
#Rendering imports
from django.urls import reverse_lazy
from django import http
#Query imports
#Other django imports
from django.contrib.auth import get_user_model, views as auth_views
from django.contrib.auth.tokens import default_token_generator
#Other imports
from django.utils.encoding import force_bytes
from django.utils import http as safehttp
from django.contrib.auth.mixins import LoginRequiredMixin

#Local imports
from . import forms
#Outside app imports
from conference import models





class HomePageView(generic.ListView):
    template_name = "home.html"
    def get_queryset(self):
        return models.Konferencija.objects.all()

#User Views
class UserCreateView(generic.CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user_create.html'

class UserUpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    template_name = 'user_update.html'
    model = get_user_model()
    login_url = reverse_lazy('login')
    fields = ['first_name','last_name','email','username']
    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs = {'pk': self.kwargs['pk']})

class UserListView(LoginRequiredMixin,generic.ListView):
    context_object_name = 'user_list'
    template_name = 'user_list.html'
    login_url = reverse_lazy('login')
    def get_queryset(self):
        sekcije = models.Sekcija.objects.filter(konferencija_id = self.kwargs['pk']).all()
        queryset = models.User_Sekcija.objects.filter(sekcija__in = sekcije).values('user').distinct()
        user_model = get_user_model()
        list =  []
        for i in queryset.all():
            if(int(i['user'])!=self.request.user.id):
                list.append(int(i['user']))
        queryset = user_model.objects.filter(id__in = list)
        return queryset

class CustomUserListView(generic.ListView):
    context_object_name = 'konf_list'
    template_name = 'custom_user_list.html'
    login_url = reverse_lazy('login')
    def get_queryset(self):
        konferencije = models.User_Sekcija.objects.filter(user_id = self.request.user.id).values('sekcija__konferencija_id').distinct()
        queryset = models.Konferencija.objects.filter(id__in = konferencije)
        return queryset

class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    login_url = reverse_lazy('login')

#Authentication views

class UserLoginView(auth_views.LoginView):
    form_class = forms.UserAuthenticationForm
    template_name = 'user_login.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('home')


class ActivationView(generic.View):
    #Activates user account and redirects to login
    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        if uidb64 is not None and token is not None:
            uid = safehttp.urlsafe_base64_decode(uidb64)
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
            valid = default_token_generator.check_token(user, token)
            try:
                if valid and not request.user.is_authenticated:
                    if user.email_confirmed == 0:
                        user_model.objects.filter(pk=uid).update(email_confirmed = 1)
                        return http.HttpResponseRedirect(reverse_lazy('login'))
                else:
                    return http.HttpResponseRedirect(reverse_lazy('home'))
            except Exception as e:
                print(e)

        return http.HttpResponseRedirect('/')

class CustomPasswordChangeView(LoginRequiredMixin,auth_views.PasswordChangeView):
    def get_success_url(self, **kwargs):
        return reverse_lazy('home')
