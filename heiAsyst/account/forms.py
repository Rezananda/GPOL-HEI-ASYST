from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import UserProfile
from django.contrib.auth.models import User


PILIH_BIRO = (
    ('pilih', 'Pilih Biro..'),
    ('DPOL','DPOL'),
    ('SSD','SSD'),
    ('SSP','SSP'),
    ('SDS','SDS'),
    ('SPO','SPO'),
    ('SSI','SSI'),
    ('BLN','BLN'),
    ('BPO 1','BPO 1'),
    ('BPO 2','BPO 2'),
    ('BSP','BSP'),
    ('CNS','CNS'),
    ('CPS','CPS'),
    ('DAS', 'DAS'),
    ('DSP', 'DSP'),
    ('EPK', 'EPK'),
    ('EPS','EPS'),
    ('KLA','KLA'),
    ('PAC','PAC'),
    ('SDS A','SDS A'),
    ('SDS B','SDS B'),
    ('SDS C','SDS C'),
    ('SDS D','SDS D'),
    ('SDS E','SDS E'),
    ('SDS F','SDS F'),
    ('SSI A','SSI A'),
    ('SSI B','SSI B'),
    ('SSI C','SSI C'),
    ('XAS','XAS'),
)

class UserProfileModelForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nama Lengkap', 'autofocus': 'autofocus'}), label=False)
    pilih_biro = forms.CharField(widget=forms.Select(choices=PILIH_BIRO), label=False)
    jumlah_member = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Jumlah Member",}), label=False)
    class Meta:
        model = UserProfile
        fields = ['full_name', 'pilih_biro', 'jumlah_member']


class UserModelForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password, minimal 5 Digit",}), label=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Konfirmasi Password",}), label=False)
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Inisial, contoh : PMR', 'maxlength' : '3'}), label=False)    
    class Meta:
        model = User

        fields = ('username', 'password1', 'password2')

