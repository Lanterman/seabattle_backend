from django.urls import path

from . import views

urlpatterns = [
    path('sign-in/', views.SignInView.as_view(), name='issue_token'),
    path('sign-up/', views.SignUpView.as_view(), name='register'),
    path("profile/<slug:username>/", views.ProfileView.as_view(), name="user-detail"),
]
