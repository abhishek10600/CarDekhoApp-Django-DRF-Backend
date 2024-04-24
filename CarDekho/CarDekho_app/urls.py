from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.car_list_view, name="car_list"),
    path("<int:pk>/", views.car_detail_view, name="car_detail"),
    path("showroom/", views.ShowRoom_View.as_view(), name="showroom_view"),
    path("showroom/<int:pk>/", views.ShowRoom_Detail.as_view(),
         name="showroom_details"),
    path("review/", views.ReviewList.as_view(), name="review_list"),
    path("review/<int:pk>", views.ReviewDetail.as_view(), name="review_details")
]
