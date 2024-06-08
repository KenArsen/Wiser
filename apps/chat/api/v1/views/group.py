from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response

from apps.chat.api.v1.serializers.group import (
    AddUserToGroupSerializer,
    GroupCreateSerializer,
    GroupDetailSerializer,
    GroupListSerializer,
    GroupUpdateSerializer,
    RemoveUserFromGroupSerializer,
)
from apps.chat.models import Group


class GroupBaseAPI(generics.GenericAPIView):
    queryset = Group.objects.all()

    def get_service(self):
        pass


class GroupListAPI(GroupBaseAPI, generics.ListCreateAPIView):
    serializer_class = GroupListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GroupDetailAPI(GroupBaseAPI, generics.RetrieveAPIView):
    serializer_class = GroupDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GroupCreateAPI(GroupBaseAPI, generics.CreateAPIView):
    serializer_class = GroupCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GroupUpdateAPI(GroupBaseAPI, generics.UpdateAPIView):
    serializer_class = GroupUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GroupDeleteAPI(GroupBaseAPI, generics.DestroyAPIView):
    serializer_class = GroupDetailSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AddUserToGroupAPI(GroupBaseAPI):
    serializer_class = AddUserToGroupSerializer

    def post(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            user_id = request.data.get("user_id")
            group.members.add(user_id)
            group.save()
            serializer = self.serializer_class(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)


class RemoveUserFromGroupAPI(GroupBaseAPI):
    serializer_class = RemoveUserFromGroupSerializer

    def post(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            user_id = request.data.get("user_id")
            group.members.remove(user_id)
            group.save()
            serializer = self.serializer_class(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)


def chat_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, "socet.html", {"group": group})
