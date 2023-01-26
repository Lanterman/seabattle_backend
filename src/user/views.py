from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from . import models as user_models, serializers


class ProfileView(RetrieveUpdateDestroyAPIView):
    """User profile endpoint"""

    queryset = user_models.User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

