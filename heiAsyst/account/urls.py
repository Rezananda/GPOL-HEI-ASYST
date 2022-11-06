from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('offline/', views.offline, name='offline'),
    # path('logout/', views.user_logout, name='logout'),
]

