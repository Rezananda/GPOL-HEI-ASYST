from django.db import models
from account.models import UserProfile
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserAttendance(models.Model):

    jumlah_sehat = models.CharField(max_length=251, null=False)
    
    jumlah_sakit = models.CharField(max_length=255, null=False)

    jumlah_member = models.CharField(max_length=255, null=False)

    authors = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.authors)

class UserSickReason(models.Model):
    
    idSick = models.ForeignKey(UserAttendance, on_delete=models.CASCADE, default=None)

    alasan_sakit = models.CharField(max_length=255, null=False)

    jumlah_alasan = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.created_at)

class UserPantun(models.Model):
    
    authors = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    kalimat_pantun = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return str(self.authors)