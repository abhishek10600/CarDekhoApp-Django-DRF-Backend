from django.contrib.auth.models import User
from rest_framework import serializers


# creating the how we create the serializer for a user
class RegisterSerializer(serializers.ModelSerializer):

    # this is used to tell the type of password_confirmation
    password_confirmation = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirmation"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    # overriding the self() method
    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password_confirmation"]

        if password != password2:
            raise serializers.ValidationError(
                {"error": "password and confirm password do not match"})

        # check if the user with the same email exists
        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError(
                {"error": "User with email already exists"})

        # create the user
        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"])
        account.set_password(password)  # hashing the password
        account.save()
        return account
