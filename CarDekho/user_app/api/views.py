from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

# we will use this to create jwt token when a user registers or creates an account
from rest_framework_simplejwt.tokens import RefreshToken


# normal user registration
# @api_view(["POST",])
# def registration_view(request):
#     if request.method == "POST":
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)


# when user creates an account it's token is generated and is logged in.
@api_view(["POST",])
def registration_view(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data["username"] = account.username
            data["email"] = account.email

            refresh = RefreshToken.for_user(account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(["POST",])
# this is how we pass authentication class in decorator or function based views
@authentication_classes([TokenAuthentication])
def logout_view(request):
    if request.method == "POST":

        # this will delete the token of the loggged in user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
