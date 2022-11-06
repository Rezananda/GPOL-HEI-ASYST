from django.contrib import admin
from .models import UserAttendance, UserSickReason, UserPantun

# Register your models here.

admin.site.register(UserAttendance)
admin.site.register(UserSickReason)
admin.site.register(UserPantun)