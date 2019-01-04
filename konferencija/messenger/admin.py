from django.contrib import admin
from . import models
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Messages, MessageAdmin)
admin.site.register(models.Messenger, MessageAdmin)
