import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from src.user.auth.models import JWTToken


@database_sync_to_async
def get_user(token: str):
    """Get user by token"""
    
    try:
        token = JWTToken.objects.get(access_token=token)
        return token.user
    except:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()

        try:
            token_key = scope["query_string"].decode().split("=")[-1]
        except ValueError:
            token_key = None

        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
