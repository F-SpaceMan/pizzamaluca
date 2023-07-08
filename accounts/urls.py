from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUp.as_view(), name="signup"),
    path('login_user', views.login_user, name='login')
]