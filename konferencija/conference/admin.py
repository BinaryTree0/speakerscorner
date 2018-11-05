from django.contrib import admin
from .models import conference

class ConferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(conference, ConferenceAdmin)
