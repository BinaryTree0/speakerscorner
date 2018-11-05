from django.shortcuts import render
from django.views.generic import CreateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ConferenceForm
from .models import conference


class ConferenceCreateView(LoginRequiredMixin, CreateView):
    form_class = ConferenceForm
    login_url = '/login/'
    template_name = 'createconference.html'
    success_url = "/conference/detail"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.chairman = form.cleaned_data['chairman']
        return super(ConferenceCreateView, self).form_valid(form)

class ConferenceListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return conference.objects.filter(creator=self.request.user)
