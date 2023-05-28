from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='issue_token'),
    path("profile/<slug:slug>/", views.ProfileView.as_view(), name="user-detail"),
]
