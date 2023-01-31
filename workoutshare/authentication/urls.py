from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/login.html'), name='logout'),
]
