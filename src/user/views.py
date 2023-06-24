from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import generics, response, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from . import models, serializers, services, permissions, db_queries
from src.game import models as game_models


class SignInView(generics.CreateAPIView):
    """Sign in endpoint"""

    serializer_class = serializers.SignInSerializer

    def post(self, request, *args, **kwargs):
        error = ValidationError(detail="Incorrect username or password.", code=status.HTTP_400_BAD_REQUEST)

        user = db_queries.get_user_by_username(request.data["username"])

        if not user:
            raise error

        if not services.validate_password(request.data["password"], user.hashed_password):
            raise error

        if not user.is_active:
            raise ValidationError(detail="Inactivate user.", code=status.HTTP_400_BAD_REQUEST)
        
        token = db_queries.create_user_token(token="1q", user=user)
        serializer = serializers.BaseTokenSerializer(token)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SignUpView(generics.CreateAPIView):
    """Sign up endpoint"""

    serializer_class = serializers.SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        serializered_token = serializers.BaseTokenSerializer(token)
        return response.Response(serializered_token.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        user = models.User.objects.create(
            hashed_password=services.create_hashed_password(self.request.data["password1"]), **serializer.data
        )
        return db_queries.create_user_token(token="1q", user=user)


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
