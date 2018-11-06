from django.contrib import admin
from .models import conference,Sekcija

class ConferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(conference, ConferenceAdmin)
admin.site.register(Sekcija, ConferenceAdmin)
