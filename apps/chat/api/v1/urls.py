from django.urls import path

from .views.group import (
    AddUserToGroupAPI,
    GroupCreateAPI,
    GroupDeleteAPI,
    GroupDetailAPI,
    GroupListAPI,
    GroupUpdateAPI,
    RemoveUserFromGroupAPI,
    chat_view,
)
from .views.message import (
    MessageCreateAPI,
    MessageDeleteAPI,
    MessageDetailAPI,
    MessageListAPI,
    MessageUpdateAPI,
)

app_name = "chats"

# group chat
urlpatterns = [
    path("groups/", GroupListAPI.as_view(), name="group-list"),
    path("groups/create/", GroupCreateAPI.as_view(), name="group-create"),
    path("groups/<int:pk>/", GroupDetailAPI.as_view(), name="group-detail"),
    path("groups/<int:pk>/update/", GroupUpdateAPI.as_view(), name="group-update"),
    path("groups/<int:pk>/delete/", GroupDeleteAPI.as_view(), name="group-delete"),
    path("groups/<int:pk>/add_user/", AddUserToGroupAPI.as_view(), name="add-user-to-group"),
    path("groups/<int:pk>/remove_user/", RemoveUserFromGroupAPI.as_view(), name="remove-user-from-group"),
    path("conect/<int:group_id>/", chat_view, name="chat-conect"),
]

# message group chat
urlpatterns += [
    path("messages/", MessageListAPI.as_view(), name="message-list"),
    path("messages/create/", MessageCreateAPI.as_view(), name="message-create"),
    path("messages/<int:pk>/", MessageDetailAPI.as_view(), name="message-detail"),
    path("messages/<int:pk>/update/", MessageUpdateAPI.as_view(), name="message-update"),
    path("messages/<int:pk>/delete/", MessageDeleteAPI.as_view(), name="message-delete"),
]
