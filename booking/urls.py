from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("accounts/logout/", views.logout_view),
    path("accounts/signup/", views.SignUp.as_view(), name="signup"),
]
