from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from users.consumers import MachineDataConsumer
from django.urls import path

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/machine-data/', MachineDataConsumer.as_asgi()),
        ])
    ),
})
