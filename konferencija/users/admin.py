#Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#Local imports
from . import models

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = UserAdmin.fieldsets +  (
            (None, {'fields': ('email_confirmed','ulica','kucni_broj','grad','drzava')}),
    )

admin.site.register(models.CustomUser, CustomUserAdmin)
