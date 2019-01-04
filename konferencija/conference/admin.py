from django.contrib import admin
from .models import Konferencija,Sekcija,User_Sekcija,Radovi

class ConferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Konferencija, ConferenceAdmin)
admin.site.register(Sekcija, ConferenceAdmin)
admin.site.register(User_Sekcija, ConferenceAdmin)
admin.site.register(Radovi, ConferenceAdmin)
