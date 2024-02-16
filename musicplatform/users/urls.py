from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="knox_login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", include("knox.urls")),
]
