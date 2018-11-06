from django.shortcuts import render
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import ConferenceForm
from .models import conference



class ConferenceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ConferenceForm
    login_url = '/login/'
    template_name = 'conference/conference_create.html'
    success_url = "/conference/detail"

    def form_valid(self, form):
        print(form.cleaned_data['model_categories'])
        print(type(form.cleaned_data['model_categories']))
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.chairman = form.cleaned_data['chairman']
        instance.sekcije = ','.join(form.cleaned_data['model_categories'])
        return super(ConferenceCreateView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

class ConferenceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = "/login/"
    def get_queryset(self):
        return conference.objects.filter(creator=self.request.user)
    def test_func(self):
        return self.request.user.is_staff

class ConferenceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = "/login/"
    model = conference
    def test_func(self):
        return self.request.user.is_staff
