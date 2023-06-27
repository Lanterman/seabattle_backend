from django.utils import timezone
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from . import models, serializers, services, permissions, db_queries
from src.game import models as game_models
from config import settings


class SignInView(generics.CreateAPIView):
    """Sign in endpoint"""

    serializer_class = serializers.SignInSerializer

    @swagger_auto_schema(responses={201: serializers.BaseJWTTokenSerializer})
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

    @swagger_auto_schema(responses={201: serializers.BaseJWTTokenSerializer})
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
            hashed_password=services.create_hashed_password(self.request.data["password1"]), **serializer.data
        )

        return services.create_jwttoken(user_id=user.id)


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
