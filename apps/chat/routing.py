from django.urls import path

from apps.chat import consumers

websocket_urlpatterns = [
    path("ws/echo/", consumers.EchoConsumer.as_asgi()),
    path("ws/users/", consumers.UserConsumer.as_asgi()),
]
