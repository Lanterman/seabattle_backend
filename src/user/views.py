from django.utils import timezone
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, response, status, views
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
            hashed_password=services.create_hashed_password(self.request.data["password1"]), 
            is_active=False,
            **serializer.data
        )

        return services.create_jwttoken(user_id=user.id, user_email=user.email)


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


class ActivateUserAccount(views.APIView):
    """Activate user account - endpoint"""

    def get(self, request, user_id: int, secret_key: str, format=None):
        _user_id = db_queries.get_user_id_by_secret_key(secret_key)

        if _user_id is None or user_id != _user_id:
            raise AuthenticationFailed(_("No user with such secret key."))

        db_queries.activate_user(user_id)

        return response.Response({"detail": "is activated."}, status=status.HTTP_200_OK)


# @user_router.put("/reset_password", status_code=status.HTTP_202_ACCEPTED)
# async def reset_password(form_data: schemas.ResetPassword, current_user: models.Users = Depends(get_current_user)):
#     """Reset password - endpoint"""

#     if not services.validate_password(form_data.old_password, current_user.password):
#         raise HTTPException(detail="Wrong old password!", status_code=status.HTTP_400_BAD_REQUEST)

#     await services.reset_password(form_data, current_user)
#     return {"detail": "Successful!", "user": schemas.BaseUser(**current_user.dict())}


# @user_router.delete("/delete_user")
# async def delete_user(back_task: BackgroundTasks, current_user: models.Users = Depends(get_current_user)):
#     """Delete user - endpoint"""

#     user = await services.delete_user(back_task=back_task, user=current_user)
#     return {"detail": "Successful!", "user_id": user}