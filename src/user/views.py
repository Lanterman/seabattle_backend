import re

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, response, status, views, decorators
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from . import models, serializers, services, permissions, db_queries
from src.game import models as game_models
from config import settings


class SignInView(generics.CreateAPIView):
    """Sign in endpoint"""

    serializer_class = serializers.SignInSerializer
    authentication_classes = []

    @swagger_auto_schema(responses={201: serializers.BaseJWTTokenSerializer}, tags=["auth"], security=[{}])
    def post(self, request, *args, **kwargs):
        error = ValidationError(detail="Incorrect username or password.", code=status.HTTP_400_BAD_REQUEST)

        user = db_queries.get_user_by_username(request.data["username"])

        if not user:
            raise error

        if not services.validate_password(request.data["password"], user.hashed_password):
            raise error
        
        if not user.is_active:
            raise ValidationError(detail="Inactivate user.", code=status.HTTP_400_BAD_REQUEST)

        token = services.create_jwttoken(user_id=user.id)
        serializer = serializers.BaseJWTTokenSerializer(token)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SignUpView(generics.CreateAPIView):
    """Sign up endpoint"""

    serializer_class = serializers.SignUpSerializer
    authentication_classes = []

    @swagger_auto_schema(responses={201: serializers.BaseJWTTokenSerializer}, tags=["auth"], security=[{}])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        serializered_token = serializers.BaseJWTTokenSerializer(token)
        return response.Response(serializered_token.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = models.User.objects.create(
            hashed_password=services.create_hashed_password(self.request.data["password1"]), 
            is_active=False,
            **serializer.data
        )

        return services.create_jwttoken(user_id=user.id, user_email=user.email)


class SignOutView(views.APIView):
    """Sign out (delete authentication jwt token) endpoint"""

    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={204: '{"detail": "Successfully logged out."}'}, tags=["auth"])
    def delete(self, request, format=None):
        instance = db_queries.get_jwttoken_instance_by_user_id(request.user.id)
        self.perform_delete(instance)
        return response.Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_delete(self, instance):
        db_queries.logout(instance)


@method_decorator(name="get", decorator=swagger_auto_schema(tags=["profile"]))
@method_decorator(name="put", decorator=swagger_auto_schema(tags=["profile"]))
@method_decorator(name="patch", decorator=swagger_auto_schema(tags=["profile"]))
@method_decorator(name="delete", decorator=swagger_auto_schema(tags=["profile"]))
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """User profile endpoint"""

    queryset = models.User.objects.all().prefetch_related(Prefetch(
        "lobbies", queryset=game_models.Lobby.objects.filter(finished_in__isnull=False)
    ))
    permission_classes = [IsAuthenticated, permissions.IsMyProfile]
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "POST"):
            if "photo" in self.request.data.keys():
                return serializers.UpdateUserPhotoSerializer
            else:
                return serializers.UpdateUserInfoSerializer
        elif self.request.method == "GET":
            if self.kwargs and self.kwargs["username"] == self.request.user.username:
                return serializers.MyProfileSerializer
            else:
                return serializers.EnemyProfileSerializer
    
    def perform_update(self, serializer):
        pre_data = {"updated_in": timezone.now()}

        if not self.request.data:
            pre_data["photo"] = ""

        serializer.save(**pre_data)


class RefreshTokenView(generics.CreateAPIView):
    """Refresh authentication JWT tokens endpoint"""

    serializer_class = serializers.RefreshJWTTokenSerializer
    authentication_classes = []
    
    @swagger_auto_schema(responses={
        201: serializers.RefreshJWTTokenSerializer, 
        400: '["Invalid refresh token."]', 
        401: '{"detail": "Refresh token expired."}',
        }, 
        tags=["auth"], 
        security=[{}],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        _token = db_queries.get_jwttoken_instance_by_refresh_token(request.data["refresh_token"])
        
        if _token.created + settings.JWT_SETTINGS["REFRESH_TOKEN_LIFETIME"] < timezone.now():
            raise AuthenticationFailed(_("Refresh token expired."))

        token = self.perform_create(_token.user_id)
        serializer = self.get_serializer(token)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, user_id: int):
        return services.create_jwttoken(user_id)


class ActivateUserAccountView(views.APIView):
    """Activate user account - endpoint"""

    authentication_classes = []

    @swagger_auto_schema(responses={
        200: '{"detail": "is activated."}', 
        401: '{"detail": "No user with such secret key."}'
        }, 
        tags=["auth"],
        security=[{}],
    )
    def get(self, request, user_id: int, secret_key: str, format=None):
        _user_id = db_queries.get_user_id_by_secret_key(secret_key)

        if _user_id is None or user_id != _user_id:
            raise AuthenticationFailed(_("No user with such secret key."))

        db_queries.activate_user(user_id)

        return response.Response({"detail": "is activated."}, status=status.HTTP_200_OK)


@method_decorator(name="put", decorator=swagger_auto_schema(tags=["profile"]))
class ResetPasswordView(generics.UpdateAPIView):
    """Reset a user account password endpoint"""

    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAccountOwner]
    serializer_class = serializers.ResetPasswordSerializer
    http_method_names = ["put", "head", "options", "trace"]
    lookup_field = "username"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not services.validate_password(request.data["old_password"], instance.hashed_password):
            raise ValidationError(detail={"old_password": "Incorrect old password."}, code=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hashed_password = services.create_hashed_password(serializer.data["new_password"])
        self.perform_update(hashed_password)
        return response.Response({"new_password": hashed_password}, status=status.HTTP_200_OK)

    def perform_update(self, hashed_password: str):
        db_queries.reset_password(self.request.user.id, hashed_password)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def get_base_username_by_token(request, *args, **kwargs):
    """Get base user info by access token to header - endpoint"""

    rex: list = re.findall(r"\w+", request.headers["Authorization"])
    username: dict = db_queries.get_base_username_by_token(rex[-2])
    return response.Response(username)
