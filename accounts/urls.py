from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignUp.as_view(), name="signup"),
    # path('userconfig/', views.UserConfig.as_view(), name="user_config")
]