from django.utils import timezone
from rest_framework import generics, response, views, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from . import models, serializers, services, permissions, db_queries


class SignInView(views.APIView):
    """Sign in endpoint"""

    def post(self, request, *args, **kwargs):
        error = ValidationError(detail="Incorrect username or password.", code=status.HTTP_400_BAD_REQUEST)

        user = db_queries.get_user_by_username(request.data["username"])

        if not user:
            raise error
        
        if not user.is_active:
            raise ValidationError(detail="Inactivate user.", code=status.HTTP_400_BAD_REQUEST)
        
        if not services.validate_password(request.data["password"], user.hashed_password):
            raise error
        
        token = db_queries.create_user_token(user=user)
        serializer = serializers.BaseTokenSerializer(token)

        return response.Response(data=serializer.data)


class SignUpView(views.APIView):
    """Sign up endpoint"""

    def post(self, request, *args, **kwargs):
        serializered_data = serializers.SignUpSerializer(data=request.data)
        serializered_data.is_valid(raise_exception=True)

        user = models.User.objects.create(hashed_password=request.data["password1"], **serializered_data.data)
        token = db_queries.create_user_token(user=user)

        serializer = serializers.BaseTokenSerializer(token)
        return response.Response(data=serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """User profile endpoint"""

    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated, permissions.IsMyProfile]
    lookup_field = "username"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH", "POST"):
            if "photo" in self.request.data.keys():
                return serializers.UpdateUserPhotoSerializer
            else:
                return serializers.UpdateUserInfoSerializer
        elif self.request.method == "GET":
            if self.kwargs["username"] == self.request.user.username:
                return serializers.MyProfileSerializer
            else:
                return serializers.EnemyProfileSerializer
    
    def perform_update(self, serializer):
        pre_data = {"updated_in": timezone.now()}

        if not self.request.data:
            pre_data["photo"] = ""

        serializer.save(**pre_data)
