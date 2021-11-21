from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.users.api.auth import serializers
from apps.users.api.auth.serializers import UserRegistrationSerializer
from apps.users.models import User


class RegisterView(CreateAPIView):
    """View to register new user."""

    queryset = User.objects.select_related().all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Register new user if data is valid."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail":
                _("Account registered.",)
             },
            status=status.HTTP_200_OK,
        )


class LoginView(KnoxLoginView):
    """View to login user with token."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """Login user and get auth token with expiry."""
        serializer = serializers.AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"])
        return super().post(request, format=None)
