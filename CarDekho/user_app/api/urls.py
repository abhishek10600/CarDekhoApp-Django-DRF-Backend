from django.urls import path

# this is used to get the token
from rest_framework.authtoken.views import obtain_auth_token

from .views import registration_view, logout_view

urlpatterns = [
    path("register/", registration_view, name="register"),
    # when we provide correct username and password of the user to this path, we get the token of the user
    path("login/", obtain_auth_token, name="login"),
    # this is the logout route and we need to pass the token of the logged in user to logout.
    path("logout/", logout_view, name="logout")
]
