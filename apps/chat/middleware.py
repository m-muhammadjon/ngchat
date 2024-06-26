import django

django.setup()

from channels.auth import AuthMiddlewareStack  # noqa
from channels.db import database_sync_to_async  # noqa
from django.contrib.auth.models import AnonymousUser  # noqa
from django.db import close_old_connections  # noqa
from rest_framework.authtoken.models import Token  # noqa


class WSAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = scope["query_string"].decode("utf-8")
        try:
            params = dict([param.split("=") for param in query_string.split("&")])
        except ValueError:
            params = dict()
        user = await self.get_user_by_token(params.get("token", ""))
        scope["user"] = user
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user_by_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()


def WSAuthMiddlewareStack(app):
    return WSAuthMiddleware(AuthMiddlewareStack(app))
