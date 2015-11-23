from django.contrib import admin
from restful.models import Lecture, Sign
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin


class MyUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'is_verified',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom info', {'fields': ('date_of_birth',)}),
        ('Beers', {'fields': ('beer',)}),
        ('Sign picture', {'fields': ('sign_pic',)}),
    )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), MyUserAdmin)

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Sign)
