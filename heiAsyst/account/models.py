from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=False)
    pilih_biro = models.CharField(max_length=255, null=False)
    jumlah_member = models.CharField(max_length=255, null=False)
    is_user = models.BooleanField(default=False, null=False)
    is_manager = models.BooleanField(default=False, null=False)
    is_admin = models.BooleanField(default=False, null=False)


    def __str__(self):
        return self.user.username
