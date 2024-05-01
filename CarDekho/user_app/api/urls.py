from django.urls import path

# this is used to get the token
from rest_framework.authtoken.views import obtain_auth_token

from .views import registration_view, logout_view

# we import this when we use we use jwt auth. These will give us access token and refresh token.
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # for token authentication
    # path("register/", registration_view, name="register"),
    # # when we provide correct username and password of the user to this path, we get the token of the user
    # path("login/", obtain_auth_token, name="login"),
    # # this is the logout route and we need to pass the token of the logged in user to logout.
    # path("logout/", logout_view, name="logout")

    #  for jwt token for authentication
    # this path is for login. It gives access token and refresh token.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # this path is used to generate new access token after previous access token is expired, with the help of refresh token.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user will register and token will get generated.
    path("register/", registration_view, name="register"),
]
