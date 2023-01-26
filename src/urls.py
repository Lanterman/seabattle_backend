from django.urls import path, include


urlpatterns = [
    path("", include("src.game.urls")),
    path("auth/", include("src.user.urls"))
]
