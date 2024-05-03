"""
ASGI config for ndtest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.urls import path

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter
from core import routing
from core.consumers import PacketConsumer,DashboardData

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ndtest.settings")

application = ProtocolTypeRouter({ 
  "http": get_asgi_application(), 
  "websocket": AuthMiddlewareStack(
        URLRouter( 
            [
            path('ws/',PacketConsumer.as_asgi()),
            path('dashboard/',DashboardData.as_asgi())
            ]
    ))
}) 
