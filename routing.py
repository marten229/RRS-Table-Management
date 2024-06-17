from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tables/', consumers.TableConsumer.as_asgi()),
]
