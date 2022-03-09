from organizations.models import OrganizationUser
from rest_framework import serializers
from rest_framework.reverse import reverse


class OrganizationUserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = ('id', 'email', 'url', 'is_admin')

    def get_email(self, obj):
        qs = obj.user
        return qs.email

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("user-detail", kwargs={"pk": obj.user.id}, request=request)

