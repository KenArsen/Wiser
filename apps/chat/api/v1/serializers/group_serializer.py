from rest_framework import serializers

from apps.chat.models import Group


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        ref_name = "GroupList"


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        ref_name = "GroupDetail"


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        ref_name = "GroupCreate"


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        ref_name = "GroupUpdate"


class AddUserToGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Group
        fields = ('user_id',)
        ref_name = "AddUserToGroup"


class RemoveUserFromGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Group
        fields = ('user_id',)
        ref_name = "RemoveUserFromGroup"
