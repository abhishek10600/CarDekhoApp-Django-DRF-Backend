# from rest_framework import serializers
# from ..models import CarList


# def alphanumeric(value):  # validators
#     if not str(value).isalnum():
#         raise serializers.ValidationError("Only alphanumeric value allowed")


# ***** SERIALIZERS *****

# class CarSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField(read_only=True)
#     # we pass the alphanumeric function from above
#     chassisnumber = serializers.CharField(validators=[alphanumeric])
#     price = serializers.DecimalField(max_digits=9, decimal_places=2)

#     # create method will first validate the data and if data is validated it will add the new data
#     def create(self, validated_data):
#         return CarList.objects.create(**validated_data)

#     # update method that will validate the data and update the existing the data
#     # instance is the existing data
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get(
#             "description", instance.description)
#         instance.active = validated_data.get("active", instance.active)
#         instance.chassisnumber = validated_data.get(
#             "chassisnumber", instance.chassisnumber)
#         instance.price = validated_data.get("price", instance.price)
#         instance.save()  # save the instance
#         return instance  # return the instance

#     # *** Performing Validations ***

#     # this is a field level validator as we name the function as validate_price which is the name of the field we are validating
#     def validate_price(self, value):  # field level validation
#         if value <= 20000.00:
#             raise serializers.ValidationError(
#                 "Price is too low, price must be greater than 20000.00")
#         return value

#     # this is object level validation. The data contains the entire object with name, description, active, chessisnumber, price
#     def validate(self, data):  # this is object level validation
#         if data["name"] == data["description"]:
#             raise serializers.ValidationError(
#                 "Name and Description cannot be same.")
#         return data


# **** MODEL SERIALIZERS ****
from rest_framework import serializers
from ..models import CarList, ShowroomList, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    # Custom
    discounted_price = serializers.SerializerMethodField()  # custom logic application

    Reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = CarList
        # fields = ["id", "name", "description"]
        fields = "__all__"
        # exclude = ["name"]

    # this method is used for discounted_price above
    def get_discounted_price(self, object):
        discountprice = object.price - 5000
        return discountprice

    # this is a field level validator as we name the function as validate_price which is the name of the field we are validating
    def validate_price(self, value):  # field level validation
        if value <= 20000.00:
            raise serializers.ValidationError(
                "Price is too low, price must be greater than 20000.00")
        return value

    # this is object level validation. The data contains the entire object with name, description, active, chessisnumber, price
    def validate(self, data):  # this is object level validation
        if data["name"] == data["description"]:
            raise serializers.ValidationError(
                "Name and Description cannot be same.")
        return data


class ShowroomSerializer(serializers.ModelSerializer):
    # nested serializer. We pass the related_name value that we used in models
    # this will give us all the information.
    # Showrooms = CarSerializer(many=True, read_only=True)

    # it will give only the filed that we provided in __str__ method in models.
    # Showrooms = serializers.StringRelatedField(many=True)

    # it will only give the primary key of the related item
    # Showrooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # it will give the link to info of the related item
    Showrooms = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='car_detail')

    class Meta:
        model = ShowroomList
        fields = "__all__"
