from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import landing_page

urlpatterns = [
    path('', views.landing_page, name = 'landing_page'),
    path('login', views.app_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
