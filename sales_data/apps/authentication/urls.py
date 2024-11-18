from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
