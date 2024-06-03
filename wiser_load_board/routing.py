from django.urls import path, include

websocket_urlpatterns = [
    path('ws/chat/', include('apps.chat.api.v1.routing')),
]