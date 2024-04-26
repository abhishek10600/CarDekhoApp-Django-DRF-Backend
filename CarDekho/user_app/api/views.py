from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


@api_view(["POST",])
def registration_view(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@api_view(["POST",])
# this is how we pass authentication class in decorator or function based views
@authentication_classes([TokenAuthentication])
def logout_view(request):
    if request.method == "POST":

        # this will delete the token of the loggged in user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
