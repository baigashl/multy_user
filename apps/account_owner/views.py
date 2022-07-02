from organizations.models import OrganizationOwner
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin

from apps.account_owner.serializers import AccountOrgOwnerSerializer


class AccountOrganizationOwnerView(CreateModelMixin, ListAPIView):
    permission_classes = []
    serializer_class = AccountOrgOwnerSerializer
    # search_fields = ('user__username', 'content')
    queryset = OrganizationOwner.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
