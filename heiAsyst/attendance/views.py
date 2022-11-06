from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from attendance.models import UserAttendance, UserSickReason, UserPantun
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.models import UserProfile
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from io import BytesIO
from django.conf import settings
from datetime import datetime
import pandas as pd
import json
import os
import xlsxwriter


# Create your views here.
@login_required
def index(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    if getUserId.is_manager == True:
        return redirect(reverse('manager_page') + '?date=now')
    elif getUserId.is_admin == True:
        return redirect('admin_page')
    else:
        try:
            getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')
            def checkAttend():
                getdate = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
                getDateCreate = timezone.localtime(getLatesAttend.created_at).strftime('%Y-%m-%d')
                if getdate == getDateCreate:
                    return 'SUDAH'
                else:
                    return 'BELUM'

            getReason = UserSickReason.objects.filter(idSick_id = getLatesAttend.id).exists()
            data = {}
            if getReason:
                getReasonList = UserSickReason.objects.filter(idSick_id = getLatesAttend.id).all()

                for i in getReasonList:
                    data[i.alasan_sakit] = i.jumlah_alasan
                    
            context = {
                'attend' : True,
                'full_name' : request.session['full_name'],
                'jumlah_sehat' : getLatesAttend.jumlah_sehat,
                'jumlah_sakit' : getLatesAttend.jumlah_sakit,
                'alasan' : data,
                'total' : getLatesAttend.jumlah_member,
                'biro' : getUserId.pilih_biro,
                'date' : getLatesAttend.created_at,
                'status_attend' : checkAttend()
            }
            return render(request, 'attendance/index.html', context)
            
        except UserAttendance.DoesNotExist:
            context = {
                'attend' : False,
                'status_attend' :'BELUM',
                'status' : 'Belum ada data terakhir',
                'biro' : getUserId.pilih_biro,
                'full_name' : request.session['full_name'],
            }
            return render(request, 'attendance/index.html', context)

@login_required()
def all_attendance(request):
    getdate = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    getAllData = UserAttendance.objects.filter(created_at__date = getdate)
    getUserName = UserProfile.objects.get(full_name = request.session['full_name'])
    getPantun = UserPantun.objects.filter(created_at__date = getdate).exists()

    getSehatSemua = []
    getSakit = []
    getAllSakit = 0
    getAllSehat = 0
    getAllMember = 0
    for i in getAllData:
        getAllSakit += int(i.jumlah_sakit)
        getAllSehat += int(i.jumlah_sehat)
        getAllMember += int(i.jumlah_member)

        getUserId = UserProfile.objects.get(user = i.authors)
        getSahatSemua = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')
        
        if getSahatSemua.jumlah_sakit == '0':
            getSehatSemua.append(getUserId.user.username + ' : ' + getSahatSemua.jumlah_sehat)
        elif getSahatSemua.jumlah_sakit != '0':
            getSakit.append(getUserId.user.username + ' (Sehat: ' + getSahatSemua.jumlah_sehat + ', Sakit: ' +getSahatSemua.jumlah_sakit + ')')

    datenow = timezone.localtime(timezone.now()).strftime('%d-%m-%Y')

    getCountDataByDate = getAllData.count()
    getCountAllUser = UserProfile.objects.filter(is_user=True).count()

    presentaseKehadiran = "%.1f%%" % (100 * getCountDataByDate/getCountAllUser)

    try:
        persentaseSakit = "%.1f%%" % (100 * getAllSakit/getAllMember)
        persentaseSehat = "%.1f%%" % (100 * getAllSehat/getAllMember)
    except ZeroDivisionError:
        persentaseSakit = "0%"
        persentaseSehat = "0%"

    if getPantun:
        context = {
            'pantun' : UserPantun.objects.get(created_at__date = getdate).kalimat_pantun,
            'pantun_status': True,
            'semua_sehat' : getSehatSemua,
            'ada_sakit' : getSakit,
            'full_name' : request.session['full_name'],
            'datenow' : datenow,
            'biro' : getUserName.pilih_biro,
            'kehadiran' : presentaseKehadiran,
            'persentaseSakit' : persentaseSakit,
            'persentaseSehat' : persentaseSehat  
        }
        return render(request, 'attendance/all_attendance.html', context)
    else:
        context = {
            'pantun_status': False,
            'semua_sehat' : getSehatSemua,
            'ada_sakit' : getSakit,
            'full_name' : request.session['full_name'],
            'datenow' : datenow,
            'biro' : getUserName.pilih_biro,
            'kehadiran' : presentaseKehadiran,
            'persentaseSakit' : persentaseSakit,
            'persentaseSehat' : persentaseSehat
        }
        return render(request, 'attendance/all_attendance.html', context)

@login_required
def my_attendance_list(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    getdateNow = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    getExist = UserAttendance.objects.exists()
    if getExist:
        getListAttendance = UserAttendance.objects.filter(authors_id = getUserId.user_id).all().order_by('-created_at')

        context = {
            'full_name' : request.session['full_name'],
            'attendance' : getListAttendance,
            'datenow' : getdateNow,
            'user_id' : getUserId.user_id,
            'url' : 'DATA SAYA',
            'back_url' : '/'
        }

        return render(request, 'attendance/my_attendance_list.html', context)
    else:
        context = {
            'full_name' : request.session['full_name'],
            'attendance' : False,
            'url' : 'DAFTAR DATA',
            'back_url' : '/'
        }

        return render(request, 'attendance/my_attendance_list.html', context)

@login_required
def my_attendance_detail(request, id):
    if request.method == 'GET':
        getAttendanceDetail = UserAttendance.objects.get(id = id)
        getReason = UserSickReason.objects.filter(idSick_id = getAttendanceDetail.id).exists()

        if getReason:
            listReason = []
            getReasonList = UserSickReason.objects.filter(idSick_id = getAttendanceDetail.id).all()

            for i in getReasonList:
                data = {
                    'alasan' : i.alasan_sakit,
                    'jumlah' : i.jumlah_alasan
                }
                
                listReason.append(data)

            listId = []
            
            for i in getReasonList:
                listId.append(i.idSick_id)

            data = {
                'message' : 'sakit',
                'alasan_sakit' : listReason,
                'idSick' : listId
            }
            return JsonResponse({'attendance':data}, status=200)
        else:
            data = {
                'message': 'sehat',
                'jumlah_sehat' : getAttendanceDetail.jumlah_sehat,
            }
            return JsonResponse({'attendance':data}, status=200)

    elif request.is_ajax and request.method == 'POST':
        getStatus = request.POST.get('status')
        getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
        attendance = UserAttendance.objects.get(id = id)

        if getStatus == 'ya':
            attendance.jumlah_sehat =getUserId.jumlah_member
            attendance.jumlah_member = getUserId.jumlah_member
            attendance.jumlah_sakit = 0
            attendance.authors = request.user
            attendance.save()

            getReason = UserSickReason.objects.filter(idSick_id = attendance.id).exists()
            
            if getStatus:
                UserSickReason.objects.filter(idSick_id = attendance.id).delete()
            
            messages.success(request, 'Berhasil ubah data')
            return JsonResponse({'message':'berhasil simpan data'}, status=200)
        
        elif getStatus == 'tidak':

            getAlasanSakit = json.loads(request.POST.get('alasan_sakit', ''))

            print(getAlasanSakit)

            tes = 0
            for datas in getAlasanSakit.values():
                tes+=datas

            getSehat = int(getUserId.jumlah_member) - tes

            attendance.jumlah_sehat = getSehat
            attendance.jumlah_sakit = tes
            attendance.authors = request.user
            attendance.jumlah_member = getUserId.jumlah_member
            attendance.save()
            
            reason = UserSickReason.objects.filter(idSick_id = id)
            reason.delete()

            for (k,v) in getAlasanSakit.items():
                reason_sick = UserSickReason(
                    idSick = attendance,
                    alasan_sakit = k,
                    jumlah_alasan = v,
                )
                reason_sick.save()

            messages.success(request, 'Berhasil ubah data')
            return JsonResponse({'message':'berhasil simpan data'}, status=200)

    else:
        print('error')

@login_required
def more(request):

    getUserData = UserProfile.objects.get(full_name = request.session['full_name'])
    
    context = {
        'full_name' : request.session['full_name'],
        'user_status' : getUserData,
        'initial' : getUserData.user.username,
        'biro' : getUserData.pilih_biro,
        'jumlah_member' : getUserData.jumlah_member,
        'id' : getUserData.id
    }
    return render(request, 'attendance/more.html', context)

@login_required
def add_attend(request):
    getStatus = request.POST.get('status')
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    attendance = UserAttendance()
    reason = UserSickReason()

    if getStatus == 'ya':
        attendance.jumlah_sehat = getUserId.jumlah_member
        attendance.jumlah_member = getUserId.jumlah_member
        attendance.jumlah_sakit = 0
        attendance.authors = request.user
        attendance.save()
        messages.success(request, 'Berhasil tambah data')
        return JsonResponse({'message':'berhasil simpan data'}, status=200)

    elif getStatus == 'tidak':
        getAlasanSakit = json.loads(request.POST.get('alasan_sakit', ''))

        tes = 0
        for datas in getAlasanSakit.values():
            tes+=datas

        getSehat = int(getUserId.jumlah_member) - tes

        attendance.jumlah_sehat = getSehat
        attendance.jumlah_sakit = tes
        attendance.jumlah_member = getUserId.jumlah_member
        attendance.authors = request.user
        attendance.save()

        for (k,v) in getAlasanSakit.items():
            reason_sick = UserSickReason(
                idSick = attendance,
                alasan_sakit = k,
                jumlah_alasan = v,
            )
            reason_sick.save()

        messages.success(request, 'Berhasil tambah data')
        return JsonResponse({'message':'berhasil simpan data'}, status=200)

@login_required
def post_pantun(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    getStatus = request.POST.get('pantun')
    pantun = UserPantun()

    pantun.kalimat_pantun = getStatus
    pantun.authors = request.user
    pantun.save()

    if getUserId.is_manager == True:
        messages.success(request, 'Berhasil tambah pantun')
        return redirect(reverse('manager_page') + '?date=now')
    else:
        messages.success(request, 'Berhasil tambah pantun')
        return redirect('all_attendance')

@login_required
def edit_account(request, id):

    userProfile = UserProfile.objects.get(id = id)

    if userProfile.full_name != request.POST.get('namaLengkah'):

        userProfile.full_name = request.POST.get('namaLengkah')
        userProfile.user.username = request.POST.get('inisial')
        userProfile.pilih_biro = request.POST.get('biro')
        userProfile.jumlah_member = request.POST.get('jumlahAnggota')
        userProfile.save()
        
        messages.success(request, 'Berhasil ubah data')
        return redirect('user_logout')
        
    else:
        userProfile.full_name = request.POST.get('namaLengkah')
        userProfile.user.username = request.POST.get('inisial')
        userProfile.pilih_biro = request.POST.get('biro')
        userProfile.jumlah_member = request.POST.get('jumlahAnggota')
        userProfile.save()
        userProfile.user.save()
        
        if userProfile.pilih_biro == 'DPOL':
            messages.success(request, 'Berhasil ubah data')
            return redirect('manager_profile')
        else:
            messages.success(request, 'Berhasil ubah data')
            return redirect('more')

@login_required
def admin_page(request):

    getUserData = UserProfile.objects.all()
    
    context = {
        'data' : getUserData
    }

    return render(request, 'attendance/admin_page.html', context)

@login_required
def admin_page_detail(request, id):
    if request.method == 'POST':
        id = request.POST.get('id')

        userStatus = UserProfile.objects.get(id = id)

        userStatus.is_user = request.POST.get('is_user').title()
        userStatus.is_manager = request.POST.get('is_manager').title()
        userStatus.is_admin = request.POST.get('is_admin').title()

        userStatus.save()

        return JsonResponse({'attendance':'berhasil'}, status=200)
    else :
        getUserData = UserProfile.objects.get(id = id)
        
        data = {
            'is_manager' : getUserData.is_manager,
            'is_user' : getUserData.is_user,
            'is_admin' : getUserData.is_admin
        }

        return JsonResponse({'attendance':data}, status=200)

@login_required
def admin_delete_member(request, id):

    users = UserProfile.objects.get(id = id)

    UserProfile.objects.get(id = id).delete()
    User.objects.get(username = users.user).delete()
    
    try:
        UserAttendance.objects.get(authors__username = users.user).delete()
    except UserAttendance.DoesNotExist:
        pass

    messages.success(request, 'Berhasil hapus data')

    return redirect('admin_page')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.warning(request, 'Please correct the error below.')
            return redirect('change_password')
    else:
        getUserData = UserProfile.objects.get(full_name = request.session['full_name'])
        if getUserData.is_manager == True:
            form = PasswordChangeForm(request.user)
            return render(request, 'attendance/change_password.html', {
                'form': form,
                'full_name' : request.session['full_name'],
                'biro' : getUserData.pilih_biro,
                'url' : 'UBAH PASSWORD',
                'back_url' : '/'
            })
        else:
            form = PasswordChangeForm(request.user)
            return render(request, 'attendance/change_password.html', {
                'form': form,
                'full_name' : request.session['full_name'],
                'biro' : getUserData.pilih_biro,
                'url' : 'UBAH PASSWORD',
                'back_url' : '/more'
            })

@login_required()
def manager_page(request):
    getDate = request.GET.get('date', '')
    getdateNow = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    getALLUserAttend = UserAttendance.objects.filter(created_at__date = getdateNow)
    getUserData = UserProfile.objects.get(full_name = request.session['full_name'])
    getPantun = UserPantun.objects.filter(created_at__date = getdateNow).exists()
    
    def checkPantun():
        if getPantun:
            data = {
                'pantun' : UserPantun.objects.get(created_at__date = getdateNow).kalimat_pantun,
                'pantun_status': True,
            }
            return data
        else:
            data = {
                'pantun_status': False,
            }
            return data 

    getListAllUserAttend = []

    for j in getALLUserAttend:
        getListAllUserAttend.append(j.authors.username)

    getAllUser = UserProfile.objects.filter(is_user=True).all()

    geListAttend = []

    for i in getAllUser:
        if i.user.username not in getListAllUserAttend:
            geListAttend.append(i.full_name)
            
    getAllData = UserAttendance.objects.filter(created_at__date = getdateNow)
    getUserName = UserProfile.objects.get(full_name = request.session['full_name'])
    getSehatSemua = []
    getSakit = []
    getAllSakit = 0
    getAllSehat = 0
    getAllMember = 0
    for i in getAllData:
        getAllSakit += int(i.jumlah_sakit)
        getAllSehat += int(i.jumlah_sehat)
        getAllMember += int(i.jumlah_member)

        getUserId = UserProfile.objects.get(user = i.authors)
        getSahatSemua = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')
        
        if getSahatSemua.jumlah_sakit == '0':
            getSehatSemua.append(getUserId.user.username + ' : ' + getSahatSemua.jumlah_sehat)
        elif getSahatSemua.jumlah_sakit != '0':
            getSakit.append(getUserId.user.username + ' (Sehat: ' + getSahatSemua.jumlah_sehat + ', Sakit: ' +getSahatSemua.jumlah_sakit + ')')

    getCountDataByDate = getAllData.count()
    getCountAllUser = UserProfile.objects.filter(is_user=True).count()
    presentaseKehadiran = "%.1f%%" % (100 * getCountDataByDate/getCountAllUser)

    try:
        persentaseSakit = "%.1f%%" % (100 * getAllSakit/getAllMember)
        persentaseSehat = "%.1f%%" % (100 * getAllSehat/getAllMember)
    except ZeroDivisionError:
        persentaseSakit = "0%"
        persentaseSehat = "0%"

    if getDate == 'now':

        getAllData = UserAttendance.objects.filter(created_at__date = getdateNow)

        sehatVal = 0
        for i in getAllData:
            sehatVal += int(i.jumlah_sehat)

        sakitVal = 0
        for i in getAllData:
            sakitVal += int(i.jumlah_sakit)

        context = {
            'check_pantun' : checkPantun(),
            'data_member' : getUserData,
            'semua_sehat' : getSehatSemua,
            'ada_sakit' : getSakit,
            'full_name' : request.session['full_name'],
            'datenow' : getdateNow,
            'jumlah_sehat' : sehatVal,
            'jumlah_sakit' : sakitVal,
            'status_data' : 'SEMUA DATA',
            'not_attend' : geListAttend,
            'filter' : 'now',
            'kehadiran' : presentaseKehadiran,
            'persentaseSakit' : persentaseSakit,
            'persentaseSehat' : persentaseSehat
        }
        return render(request, 'attendance/manager_page.html', context)

    elif getDate == 'all':

        getAllData = UserAttendance.objects.filter()

        sehatVal = 0
        for i in getAllData:
            sehatVal += int(i.jumlah_sehat)

        sakitVal = 0
        for i in getAllData:
            sakitVal += int(i.jumlah_sakit)

        context = {
            'check_pantun' : checkPantun(),
            'data_member' : getUserData,
            'semua_sehat' : getSehatSemua,
            'ada_sakit' : getSakit,
            'full_name' : request.session['full_name'],
            'datenow' : getdateNow,
            'jumlah_sehat' : sehatVal,
            'jumlah_sakit' : sakitVal,
            'status_data' : 'SEMUA DATA',
            'not_attend' : geListAttend,
            'filter' : 'all',
            'kehadiran' : presentaseKehadiran,
            'persentaseSakit' : persentaseSakit,
            'persentaseSehat' : persentaseSehat
        }
        return render(request, 'attendance/manager_page.html', context)

    else:

        getAllData = UserAttendance.objects.filter(created_at__date = getDate)

        sehatVal = 0
        for i in getAllData:
            sehatVal += int(i.jumlah_sehat)

        sakitVal = 0
        for i in getAllData:
            sakitVal += int(i.jumlah_sakit)

        context = {
            'check_pantun' : checkPantun(),
            'data_member' : getUserData,
            'semua_sehat' : getSehatSemua,
            'ada_sakit' : getSakit,
            'full_name' : request.session['full_name'],
            'datenow' : getdateNow,
            'jumlah_sehat' : sehatVal,
            'jumlah_sakit' : sakitVal,
            'status_data' : 'DATA ' + getDate,
            'not_attend' : geListAttend,
            'filter' : 'date',
            'kehadiran' : presentaseKehadiran,
            'persentaseSakit' : persentaseSakit,
            'persentaseSehat' : persentaseSehat
        }
        return render(request, 'attendance/manager_page.html', context)

@login_required
def manager_profile(request):

    getUserData = UserProfile.objects.get(full_name = request.session['full_name'])
    
    context = {
        'data_member' : getUserData,
    }
    return render(request, 'attendance/manager_profile.html', context)

@login_required
def download_to_excel(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])

    data = UserAttendance.objects.filter(authors_id = getUserId.user_id).order_by('-created_at')

    id_data = []
    jumlah_sehat = [] 
    jumlah_sakit = []
    jumlah_member = []
    created_at_date = []
    created_at_time = []

    id_foreign = []
    alasan_sakit = []
    jumlah_alasan = []
    created_at_date_alasan = []
    created_at_time_alasan = []

    for b in data:
        id_data.append(b.id)
        jumlah_sehat.append(b.jumlah_sehat)
        jumlah_sakit.append(b.jumlah_sakit)
        jumlah_member.append(b.jumlah_member)
        getDateTime = timezone.localtime(b.created_at)
        created_at_date.append(getDateTime.strftime('%Y-%m-%d'))
        created_at_time.append(getDateTime.strftime('%H:%M'))

        dataAlasan = UserSickReason.objects.filter(idSick_id = b.id).order_by('-created_at')
        for c in dataAlasan:
            id_foreign.append(c.idSick.id)
            alasan_sakit.append(c.alasan_sakit)
            jumlah_alasan.append(c.jumlah_alasan)
            getDateTime = timezone.localtime(c.created_at)
            created_at_date_alasan.append(getDateTime.strftime('%Y-%m-%d'))
            created_at_time_alasan.append(getDateTime.strftime('%H:%M'))

    allData = {
        'ID' : id_data,
        'Tanggal Isi' : created_at_date,
        'Waktu Isi' : created_at_time,
        'Jumlah Sehat' : jumlah_sehat,
        'Jumlah Sakit' : jumlah_sakit,
        'Jumlah Member' : jumlah_member,
    }

    allReason = {
        'ID Foreign Key' : id_foreign,
        'Tanggal Isi' : created_at_date_alasan,
        'Waktu Isi' : created_at_time_alasan,
        'Alasan Sakit' : alasan_sakit,
        'Jumlah Alasan' : jumlah_alasan
    }

    df = pd.DataFrame(allData, columns = ['ID', 'Tanggal Isi', 'Waktu Isi', 'Jumlah Sehat' , 'Jumlah Sakit', 'Jumlah Member'])
    df2 = pd.DataFrame(allReason, columns = ['ID Foreign Key', 'Tanggal Isi', 'Waktu Isi', 'Alasan Sakit' , 'Jumlah Alasan'])
    print("awal")

    writer = pd.ExcelWriter('/var/www/web_env/env1/heiAsyst/dataanggota.xlsx', engine='xlsxwriter')
    print("akhir")
    df.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')

    writer.save()
    # response = HttpResponse(open("C:/Users/Reza Nanda/Documents/DPOL-Project/heiAsyst/dataanggota.xlsx", 'rb').read())
    # response = HttpResponse(open("/app/dataanggota.xlsx", 'rb').read())
    response = HttpResponse(open("/var/www/web_env/env1/heiAsyst/dataanggota.xlsx", 'rb').read())
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename=dataanggota.xlsx'
    return response

@login_required
def user_logout(request):
    try:
        del request.session['full_name']
        logout(request)
    except KeyError:
        pass

    return redirect('user_login')
