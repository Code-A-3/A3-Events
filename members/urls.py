from . import views
from django.urls import path

urlpatterns = [
    path('login_user', views.login_user, name="login-user"),
    path('logout_user', views.logout_user, name="logout-user"),
    path('register_user', views.register_user, name="register-user"),
]
