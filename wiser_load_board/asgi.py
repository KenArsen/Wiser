import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiser_load_board.settings")

django_asgi_app = get_asgi_application()
from apps.chat.middleware import JWTAuthMiddleware
from apps.chat.api.v1.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
})
