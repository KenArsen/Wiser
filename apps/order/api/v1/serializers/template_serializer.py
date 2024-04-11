from rest_framework import serializers

from apps.order.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ["id", "is_active", "content", "logo_url"]
        ref_name = "Template"

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
