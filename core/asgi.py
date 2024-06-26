import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.chat.middleware import WSAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import apps.chat.routing  # noqa

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WSAuthMiddlewareStack(URLRouter(apps.chat.routing.websocket_urlpatterns)),
    }
)
