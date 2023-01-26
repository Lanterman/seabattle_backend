from django.urls import path

from . import views

urlpatterns = [
    path("profile/<slug:slug>/", views.ProfileView.as_view(), name="user-detail"),
]
