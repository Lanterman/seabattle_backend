import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .middlewares import TokenAuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from src.game import routings as game_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter(
                game_routing.websocket_urlpatterns,
            )
        )
    )
})
