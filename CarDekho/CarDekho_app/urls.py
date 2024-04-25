from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# this router is used to combine same type of urls into one
# for example showroom/ and showroom/2 these two urls will be handled.
router = DefaultRouter()
# router.register("showroom", views.Showroom_Viewset, basename="showroom")
router.register("showroom", views.Showroom_ModelViewSet, basename="showroom")

urlpatterns = [
    path("list/", views.car_list_view, name="car_list"),
    path("<int:pk>/", views.car_detail_view, name="car_detail"),
    path("", include(router.urls)),  # showroom/ and showroom/2
    # path("showroom/", views.ShowRoom_View.as_view(), name="showroom_view"),
    # path("showroom/<int:pk>/", views.ShowRoom_Detail.as_view()),
    #      name="showroom_details"),
    # path("review/", views.ReviewList.as_view(), name="review_list"),
    # path("review/<int:pk>", views.ReviewDetail.as_view(), name="review_details")


    # creating review for a particular car in the showroom. This is pk is the primary key of the car
    # basically create reviews of a particular car
    path("showroom/<int:pk>/review-create",
         views.ReviewCreate.as_view(), name="review_create"),
    # show the review of a car in the showroom. This is pk is the primary of the car
    # shhow the reviews of a particualr car
    path("showroom/<int:pk>/review",
         views.ReviewList.as_view(), name="review_list"),
    # show the review of by the pk. This pk is the primary key of the review.
    path("showroom/review/<int:pk>", views.ReviewDetail.as_view(), name="")

]
