#View imports
from django.views import generic
#Rendering imports
from django.shortcuts import redirect
from django.urls import reverse_lazy
#Query imports
from django.db.models import Q
#Other django imports
from django.contrib.auth import get_user_model
#Other imports
import math
#Local imports
from . import models

#Main views
class MessageList(generic.ListView):
    template_name = 'message-list.html'
    def get(self, request, *args, **kwargs):
        #Added
        #Get user model. If user connection doesnt exist create user connection
        user_model = get_user_model()
        messenger = models.Messenger.objects.filter(sender = self.request.user , reciever_id = self.kwargs['pk'])
        if(not messenger.exists()):
            models.Messenger.objects.create(sender = self.request.user, reciever = user_model.objects.filter(id = self.kwargs['pk']).get())
        #Usual
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()

        #Get number from which last 18 messages will be shown
        return self.render_to_response(context)

    #Returns queryset which contains all messages between two users
    def get_queryset(self):
        queryset = models.Messages.objects.filter((Q(messenger__sender_id = self.request.user.id) & Q(messenger__reciever_id = self.kwargs['pk']))| (Q(messenger__sender_id = self.kwargs['pk']) & Q(messenger__reciever_id = self.request.user.id))).order_by('-id')
        return queryset

    #Saves message and reloads page
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if(request.POST['message'].replace(' ','').replace("\r\n","")!=""):
            print("hello")
            messenger = models.Messenger.objects.filter(sender = self.request.user , reciever_id = self.kwargs['pk']).get()
            models.Messages.objects.create(messenger = messenger,message = self.request.POST['message'])
        return redirect(reverse_lazy('messenger:messenger', kwargs={ 'pk': self.kwargs['pk'] }))
