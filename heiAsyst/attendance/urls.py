from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-attend/', views.all_attendance, name='all_attendance'),
    # path('my-attend/', views.my_attendance, name='my_attendance'),
    path('my-attend-list/', views.my_attendance_list, name='my_attendance_list'),
    path('my-attend-list/<int:id>/', views.my_attendance_detail, name='my_attendance_detail'),
    # path('my-attend-list-edit/<int:id>/', views.my_attendance_edit, name='my_attendance_edit'),
    path('more/', views.more, name='more'),
    path('manager-profile/', views.manager_profile, name='manager_profile'),
    path('add-attend/', views.add_attend, name='add_attend'),
    # path('add-edit-attend-post/', views.add_edit_attend_post, name='add_edit_attend_post'),
    path('manager/', views.manager_page, name='manager_page'),
    # path('manager/<int:id>/', views.manager_member_detail, name='manager_member_detail'),
    path('logout/', views.user_logout, name='user_logout'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('admin-page/<int:id>/', views.admin_page_detail, name='admin_page_detail'),
    path('admin-page/delete/<int:id>/', views.admin_delete_member, name='admin_delete_member'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('download-to-excel/', views.download_to_excel, name='download_to_excel'),
    path('edit-account/<int:id>/', views.edit_account, name='edit_account'),
    path('change-password/', views.change_password, name='change_password'),
    path('download-to-excel/', views.download_to_excel, name='download_to_excel'),
    path('post-pantun/', views.post_pantun, name='post_pantun'),
]