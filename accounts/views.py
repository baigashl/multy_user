from rest_framework.generics import (
    RetrieveAPIView, ListAPIView, CreateAPIView
)
from rest_framework.mixins import (
    UpdateModelMixin,
    DestroyModelMixin, CreateModelMixin,
)
from organizations.models import (
    Organization, OrganizationOwner, OrganizationUser
)
from rest_framework.authentication import SessionAuthentication
from accounts.serializers import (
    AccountDetailSerializers,
    AccountSerializers, OrganizationCreateSerializer, ImageSerializer,
)


class OrganizationListAPIView(CreateModelMixin, ListAPIView):
    # permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    queryset = Organization.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        old_obj = self.request.data
        org = serializer.save()
        user = self.request.user
        org_user = OrganizationUser.objects.create(
            user=user,
            organization=org
        )
        org_owner = OrganizationOwner.objects.create(
            organization_user=org_user,
            organization=org
        )
        serializer.save(organization_user=org_user, organization_owner=org_owner)


class OrganizationCreateAPIView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Organization.objects.all()
    serializer_class = OrganizationCreateSerializer


class AccountDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    permission_classes = []
    authentication_classes = [SessionAuthentication]
    queryset = Organization.objects.all()
    serializer_class = AccountDetailSerializers
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
