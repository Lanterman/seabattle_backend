from django.urls import path

from . import oauth_views

urlpatterns = [

    path("github/", oauth_views.AuthGitHubView.as_view(), name="sign-in-github"),
]


