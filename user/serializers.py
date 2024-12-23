from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exists = User.objects.filter(username=attrs["username"]).exists()

        errors = {}

        if email_exists:
            errors["email"] = "Email has already been used."

        if username_exists:
            errors["username"] = "Username has already been used."

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user
