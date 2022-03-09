from organizations.models import Organization
from rest_framework import serializers
from rest_framework.reverse import reverse



class AccountInlineSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id',
            'url',  #
            'name',
            'owner',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail", kwargs={"id": obj.id}, request=request)
