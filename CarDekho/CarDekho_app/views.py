from django.shortcuts import render
from .models import CarList, ShowroomList, Review
from .api_file.serializers import CarSerializer, ShowroomSerializer, ReviewSerializer
from .api_file.permissions import AdminOrReadOnlyPermission, ReviewUserOrReadOnlyPermission
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

# importing the JWTAuthentication and we can use it where we want jwt auth.
from rest_framework_simplejwt.authentication import JWTAuthentication

# from django.http import JsonResponse
# from django.http import HttpResponse
# import json

# Create your views here.


# creating rest api only with django
# def car_list_view(request):
#     cars = CarList.objects.all()
#     data = {
#         "cars": list(cars.values()),
#     }
#     # return JsonResponse(data)
#     data_json = json.dumps(data)
#     return HttpResponse(data_json, content_type="application/json")


# def car_detail_view(request, pk):
#     car = CarList.objects.get(pk=pk)
#     data = {
#         "name": car.name,
#         "description": car.description,
#         "active": car.active
#     }

#     return JsonResponse(data)

# *****************************************************************************


# ***** GENERICS VIEWS AND MIXINS *****
# Generic views are used when we want basic post, get and other methods with no customization and control.
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     authentication_classes = [SessionAuthentication]
#     # DjangoModelPermission is used to provide permissions to specific user. It can only be used in views that have a queryset or get_queyset
#     permission_classes = [DjangoModelPermissions]

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# *********************************************************************


# ***** CONCRETE CLASSES *****
# CONCRETE CLASSES are built using the mixins and the generic views

# use concreate classes when working on an api that uses foreign relationships.
class ReviewCreate(generics.CreateAPIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        cars = CarList.objects.get(pk=pk)

        # we can get the information of the logged in user using self.request.user
        useredit = self.request.user
        # we want one user to review only once
        Review_queryset = Review.objects.filter(car=cars, apiuser=useredit)
        if Review_queryset.exists():
            raise ValidationError("Your review already exists.")
        serializer.save(car=cars, apiuser=useredit)


class ReviewList(generics.ListAPIView):

    # authentication_classes = [SessionAuthentication]
    # DjangoModelPermission is used to provide permissions to specific user. It can only be used in views that have a queryset or get_queyset
    # permission_classes = [DjangoModelPermissions]

    # queryset = Review.objects.all()
    # serializer_class = ReviewSerializer

    serializer_class = ReviewSerializer

    # we need to pass the token in the authorization header.
    authentication_classes = [JWTAuthentication]  # applying jwt authentication

    # applying the custom permissions that we created in permissions.py file
    # permission_classes = [AdminOrReadOnlyPermission]
    permission_classes = [IsAuthenticated,]

    # get the review of a car py the primary key of the car

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(car=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # we need to pass the token in the authorization header.
    authentication_classes = [TokenAuthentication]

    # applying the custom permissions that we created in permissions.py file
    # permission_classes = [AdminOrReadOnlyPermission]
    permission_classes = [ReviewUserOrReadOnlyPermission]

# ***********************************************************************


# ***** Class Based Views *****
class ShowRoom_View(APIView):

    # applying authentication
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]

    # session authentication
    # we use the authentication_classes and permission_classes in all the views where we want authentication and permission
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        showroom = ShowroomList.objects.all()
        serializer = ShowroomSerializer(
            showroom, many=True, context={"request": request})  # we pass the context because in serializer we are using the nested serializer and we are using HyperlinkedRelatedField. If we are not using the HyperlinkedRelatedField should remove the context from the argument.
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ShowRoom_Detail(APIView):
    def get(self, request, pk):
        try:
            showroom = ShowroomList.objects.get(pk=pk)
        except ShowroomList.DoesNotExist:
            return Response({
                "error": "Showroom not found"
            }, status=status.HTTP_404_NOT_FOUND)
        # we pass the context because in serializer we are using the nested serializer and we are using HyperlinkedRelatedField. If we are not using the HyperlinkedRelatedField should remove the context from the argument.
        serializer = ShowroomSerializer(showroom, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            showroom = ShowroomList.objects.get(pk=pk)
        except ShowroomList.DoesNotExist:
            return Response({
                "error": "Showroom not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            showroom = ShowroomList.objects.get(pk=pk)
        except ShowroomList.DoesNotExist:
            return Response({
                "error": "Showroom not found"
            }, status=status.HTTP_404_NOT_FOUND)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# *******************************************************************************

# ***** Function Based Views *****


@api_view(["GET", "POST"])
def car_list_view(request):
    if request.method == "GET":
        try:
            car = CarList.objects.all()
        except:
            return Response({
                "Error:", "Car not found"
            }, status=status.HTTP_404_NOT_FOUND)
        # using car serializer and passing the car and many=True because we can have multiple data
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)

    # this is used to post some data and store it in our database
    if request.method == "POST":
        serializer = CarSerializer(data=request.data)  # serializing the data
        if serializer.is_valid():  # if the data is valid we save it and if data is not valid we retunr error
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def car_detail_view(request, pk):  # the pk is taken from the url so its a parameter
    if request.method == "GET":
        try:
            car = CarList.objects.get(pk=pk)
        except:
            return Response({
                "Error": "Car not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    if request.method == "PUT":
        car = CarList.objects.get(pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        car = CarList.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# *************************************************************************************

# ***** VIEWSET *****
# view set is another way to develop CRUD APIs


class Showroom_Viewset(viewsets.ViewSet):

    def create(self, request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = ShowroomList.objects.all()
        serializer = ShowroomSerializer(queryset, many=True,)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ShowroomList.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ShowroomSerializer(user)
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

# ***********************************************************************************

# **** MODELVIEWSET ****
# Model Viewset using mixins and it allows all the CRUD operations in the api.


class Showroom_ModelViewSet(viewsets.ModelViewSet):

    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = ShowroomList.objects.all()
    serializer_class = ShowroomSerializer
