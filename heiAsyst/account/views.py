from django.shortcuts import render, redirect
from account.models import UserProfile
from django.contrib import messages
from .forms import UserModelForm, UserProfileModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('inisial')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            user_status = UserProfile.objects.get(user = user)
            if user_status.is_user or user_status.is_manager == True or user_status.is_admin == True:
                request.session['full_name'] = user_status.full_name
                # request.session.set_expiry(0)
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Akun anda belum aktif.')
                return redirect('user_login')
        else:

            messages.warning(request, 'Inisial atau password anda salah.')

            return redirect('user_login')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')

        return render(request, 'account/login.html')

def register(request):
    if request.method == 'POST':
        user_form = UserModelForm(request.POST)
        profile_form = UserProfileModelForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            # user.save()
            
            profile = profile_form.save(commit=False)

            profile.user = user
            profile.save()

            messages.success(request, 'Registrasi berhasil, hubungi Admin untuk aktivasi akun anda.')
            
            return redirect('user_login')
        else:
            messages.warning(request, 'Input tidak valid.')
            return redirect('register')

    elif request.method == 'GET':

        if request.user.is_authenticated:
            return redirect('index')

        form = UserModelForm()
        profile_form = UserProfileModelForm()
        
        context = {
            'form' : form,
            'profile_form' : profile_form}
        return render(request, 'account/register.html', context)

def offline(request):
    return render(request, 'account/offline.html')