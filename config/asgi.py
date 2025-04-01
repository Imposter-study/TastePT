import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import chatbot.routing

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": SessionMiddlewareStack(
            AuthMiddlewareStack(URLRouter(chatbot.routing.websocket_urlpatterns))
        ),
    }
)
