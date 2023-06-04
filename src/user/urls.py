from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='issue_token'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    path("profile/<slug:username>/", views.ProfileView.as_view(), name="user-detail"),
]
