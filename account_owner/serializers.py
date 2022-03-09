from organizations.models import OrganizationOwner
from rest_framework import serializers
from rest_framework.reverse import reverse

from users.models import CustomUser
from users.serializers import UserAccountSerializer


class AccountOrgOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationOwner
        fields = ['organization_user', 'organization']


class OrganizationOwnerInlineSerializer(serializers.ModelSerializer):
    # url = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrganizationOwner
        fields = [
            # 'id',
            # 'url',
            'user'
        ]

    def get_user(self, obj):
        qs = CustomUser.objects.filter(
            organizations_organizationuser=obj.id
        )
        return UserAccountSerializer(qs, many=True).data

