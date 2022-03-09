from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
    OrganizationOwner
)

from account_owner.serializers import OrganizationOwnerInlineSerializer
from users.users_nested.serializers import OrganizationUserSerializer


class AccountDetailSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)  #
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'url',  #
            'id',
            'name',
            'user',
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail", kwargs={"id": obj.id}, request=request)

    def get_user(self, obj):
        qs = OrganizationUser.objects.filter(
            organization=obj
        )
        return OrganizationUserSerializer(qs, many=True).data


class AccountSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    owner = OrganizationOwnerInlineSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'url',  #
            'id',
            'name',
            'owner'
        ]
        read_only_fields = ['owner']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)


class OrganizationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['name']

