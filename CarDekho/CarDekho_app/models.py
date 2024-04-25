from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


def alphanumeric(value):  # validators
    if not str(value).isalnum():
        raise ValidationError("Only alphanumeric value allowed")


# Create your models here.


class ShowroomList(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class CarList(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(
        max_length=100, blank=True, null=True, validators=[alphanumeric])
    price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(
        ShowroomList, on_delete=models.CASCADE, related_name="Showrooms", null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    # adding the apiuser field so that we can see which user created the review
    apiuser = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MaxValueValidator, MinValueValidator])
    comments = models.CharField(max_length=200, null=True)
    car = models.ForeignKey(CarList, on_delete=models.CASCADE,
                            related_name="Reviews", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"the rating of {self.car.name}: {str(self.rating)}"
