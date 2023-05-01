from rest_framework import generics, response, views

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from . import models as user_models, serializers, services


class LoginView(views.APIView):

    def post(self, request, *args, **kwargs):
        error = ValidationError(detail="Incorrect username or password.")

        user = services.get_user_by_username(request.data["username"])

        if not user:
            raise error
        
        if not user.is_active:
            raise ValidationError(detail="Inactivate user.")
        
        if not services.validate_password(request.data["password"], user.hashed_password):
            raise error
        
        
        token = services.create_user_token(user=user)
        serializer = serializers.BaseTokenSerializer(token)

        return response.Response(data=serializer.data)
        


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """User profile endpoint"""

    queryset = user_models.User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

