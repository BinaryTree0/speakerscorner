from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import ConferenceForm,SekcijaForm,UploadFileForm
from .models import Konferencija,Sekcija,User_Sekcija,Radovi
from django.template import RequestContext
from django.db.models import Max
from django.http import HttpResponse
from . import utils
import zipfile
import datetime
#Conference
class ConferenceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ConferenceForm
    login_url = reverse_lazy('login')
    template_name = 'conference/konferencija_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form, questions):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.chairman = form.cleaned_data['chairman']
        instance.sekcije = ','.join(form.cleaned_data['model_categories'])
        instance.form = questions
        return super(ConferenceCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        questions = []
        self.object = None
        questions = request.POST.getlist('question')
        questions = list(filter(None, questions))
        if(len(questions)!=0):
            questions = ','.join(questions)
            questions = questions
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            return self.form_valid(form, questions)
        else:
            return self.form_invalid(form)

    def test_func(self):
        return self.request.user.is_staff


class ConferenceListView(LoginRequiredMixin, ListView):
    template_name = "conference/konferencija_list.html"
    login_url = reverse_lazy('login')
    def get_queryset(self):
        queryset = []
        userList = User_Sekcija.objects.filter(user_id = self.request.user.id).all()
        chairmanList = Konferencija.objects.filter(chairman = self.request.user)
        for i in userList:
            if i.sekcija.konferencija not in queryset:
                queryset.append(i.sekcija.konferencija)
        for i in chairmanList:
            if i not in queryset:
                queryset.append(i)
        queryset = sorted(queryset, key=lambda x: x.time)
        return queryset

class ConferenceDetailView(DetailView):
    model = Konferencija
    def get_context_data(self, **kwargs):
        object = super().get_context_data(**kwargs)
        object['sekcije'] = Sekcija.objects.filter(konferencija = object['konferencija']).all()
        if(self.request.user.is_authenticated):
            dict = {}
            for i in object['sekcije']:
                recenzent = User_Sekcija.objects.filter(user=self.request.user,sekcija = i)
                if(recenzent.exists()):
                    print(recenzent)
                    recenzent = recenzent.get()
                    if(recenzent.recenzent_approved == 1):
                        dict[i] = True
                    else:
                        dict[i] = False
                else:
                    dict[i] = False
            print(dict)
            object['dict'] = dict.items()
        return object


class SekcijeDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Sekcija
    def get_context_data(self, **kwargs):
        object = super().get_context_data(**kwargs)
        object['Sekcija'] = Sekcija.objects.filter(id = int(self.kwargs['pk'])).get()
        tz_info = object['Sekcija'].konferencija.time.tzinfo
        time = (datetime.datetime.now(tz_info) - object['Sekcija'].konferencija.time).days
        object['Time'] = 30 - time
        object['Rad'] = Radovi.objects.filter(user_sekcija__sekcija_id = int(self.kwargs['pk']),user_sekcija__user_id = self.request.user.id).last()
        if(object['Rad']):
            object['State']= utils.Ocjene[object['Rad'].approved]
        else:
            object['State']= None
        if(time < 30):
            object['Bool'] = True
        else:
            object['Bool'] = False
        try:
            object['registered'] =  User_Sekcija.objects.filter(user = self.request.user,sekcija = object['Sekcija']).get()
        except:
            object['registered'] = None
        return object


class SekcijeCreateView(LoginRequiredMixin, CreateView):
    form_class = SekcijaForm
    login_url = reverse_lazy('login')
    template_name = 'conference/sekcija_create.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Sekcija'] = Sekcija.objects.filter(id = int(self.kwargs['pk'])).get()
        context['Konferencija'] = Konferencija.objects.filter(id = context['Sekcija'].konferencija.id).get()
        list = context['Konferencija'].form.split(',')
        if(len(list)>1):
            context['Konferencija'].form = list
        else:
            context['Konferencija'].form = ''
        return context

    def form_valid(self, form, questions):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.sekcija = Sekcija.objects.filter(id = int(self.kwargs['pk'])).get()
        instance.recenzent_not_approved = form.cleaned_data['recenzent']
        instance.questions = questions
        return super(SekcijeCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        questions = ''
        for i in request.POST:
            if('question' in i):
                questions = questions + '['+ i + ':' + request.POST[i]+']' + '|'
        questions = questions[0:len(questions)-1]
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form,questions)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        url = reverse_lazy('conference:sekcija', kwargs={'pk': self.kwargs['pk']})
        return url

class SekcijeView(View):
    def get(self, request, *args, **kwargs):
        bool = User_Sekcija.objects.filter(user = self.request.user, sekcija_id = kwargs['pk'])
        if not bool:
            view = SekcijeCreateView.as_view()
        else:
            view = SekcijeDetailView.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = SekcijeCreateView.as_view()
        return view(request, *args, **kwargs)

class FileCreateView(LoginRequiredMixin, CreateView):
    form_class = UploadFileForm
    login_url = reverse_lazy('login')
    template_name = 'conference/file_create.html'
    def post(self, request, *args, **kwargs):
        self.object = None
        user_sekcija = User_Sekcija.objects.filter(id = self.kwargs['pk']).get()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form,user_sekcija)
        else:
            return self.form_invalid(form)
    def get_success_url(self):
        id = User_Sekcija.objects.filter(id = self.kwargs['pk']).get().sekcija.id
        self.success_url = reverse_lazy('conference:sekcija', kwargs={'pk': id})
        return str(self.success_url)

    def form_valid(self, form, user_sekcija):
        instance = form.save(commit=False)
        print(instance.upload)
        instance.user_sekcija = user_sekcija
        return super(FileCreateView, self).form_valid(form)

class RadoviListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    def get_queryset(self):
        radovi = Radovi.objects.filter(user_sekcija__sekcija_id = self.kwargs['pk'],user_sekcija__recenzent_approved = 0)
        users = radovi.values('user_sekcija').distinct()
        queryset = Radovi.objects.none()
        for i in users:
            query = radovi.filter(user_sekcija_id = i['user_sekcija'])
            max_pk = query.aggregate(Max('id'))['id__max']
            query = query.filter(id = max_pk)
            queryset = queryset | query
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bool'] = User_Sekcija.objects.filter(user_id=self.request.user.id,sekcija_id=self.kwargs['pk']).get().recenzent_approved
        context['Id'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        if('path' in request.POST):
            path = request.POST['path']
            rad = Radovi.objects.filter(upload = path)
            bool = User_Sekcija.objects.filter(sekcija_id = self.kwargs['pk'],user_id = self.request.user.id).get().recenzent_approved
            if(rad.get().approved == 0 and bool == 1):
                rad.update(approved = 1)
            with open(path, 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'filename=some_file.pdf'
                return response
        elif('all' in request.POST):
            filenames = request.POST.getlist('all')
            zipfile_name = 'pdf_docs.zip'
            response = HttpResponse(content_type='application/zip')
            zip_file = zipfile.ZipFile(response, 'w')
            for filename in filenames:
                zip_file.write(filename)
            response['Content-Disposition'] = 'attachment; filename={}'.format(zipfile_name)
            return response
        else:
            value = 0
            for i in request.POST:
                if('choose' in i):
                    value = int(request.POST[i])
                    id = int(i.split('_')[0])
                    break

            Radovi.objects.filter(id = id).update(approved = value)
            return self.get(self, request, *args, **kwargs)

class RecenzentListView(LoginRequiredMixin,ListView):
    context_object_name = 'recenzent_list'
    template_name = 'conference/recenzent_list.html'
    login_url = reverse_lazy('login')
    def get_queryset(self):
        sekcije = Sekcija.objects.filter(konferencija_id = self.kwargs['pk']).all()
        queryset = User_Sekcija.objects.filter(sekcija__in = sekcije,recenzent_not_approved=1)
        return queryset
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if(request.POST['bool'] == "true"):
            queryset.filter(id=request.POST['user']).update(recenzent_not_approved=0,recenzent_approved = 1)
        else:
            queryset.filter(id=request.POST['user']).update(recenzent_not_approved=0,recenzent_approved = 0)
        return self.get(self, request, *args, **kwargs)
