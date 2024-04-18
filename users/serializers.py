from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
        }


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        ]
