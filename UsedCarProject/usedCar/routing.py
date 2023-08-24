from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path('contract', consumers.ChatConsumer.as_asgi()),
]

channel_routing = []