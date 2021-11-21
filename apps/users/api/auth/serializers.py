from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.api.serializers import UserSerializer
from apps.users.models import User
from libs.open_api.serializers import OpenApiSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    email = serializers.EmailField(
        help_text="Email of user which singing up.",
    )
    password = serializers.CharField(
        max_length=128,
    )
    password_confirm = serializers.CharField(
        max_length=128,
    )

    class Meta:
        model = User
        fields = (
            "password",
            "password_confirm",
            "email",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        """Validate email and password."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password": "Password fields didn't match.",
            })
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({
                "email": "User with this email is already registered.",
            })

        return attrs

    def create(self, validated_data: dict):
        """Create user account and send confirmation email."""
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.

    Copied form rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    email = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        """Validate that user with provided credentials."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict):
        """Escape warning."""

    def update(self, instance, validated_data):
        """Escape warning."""


class TokenSerializer(OpenApiSerializer):
    """Auth token for entire app."""

    expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.REST_KNOX['TOKEN_TTL']}",
    )
    token = serializers.CharField(help_text="Token itself")
    user = UserSerializer()
