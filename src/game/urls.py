from django.urls import path
from . import views

urlpatterns = [
    path("lobbies/", views.LobbyListView.as_view(), name='lobby-list'),
    path("lobbies/<slug:slug>/", views.DetailLobbyView.as_view(), name="lobby-detail"),
    path("leadboard/", views.LeadBoardView.as_view(), name="leadboard")
]
