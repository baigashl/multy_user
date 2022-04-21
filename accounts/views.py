from rest_framework import mixins
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

from accounts.models import Category, Account
from accounts.serializers import (
    AccountDetailSerializers,
    AccountSerializers,
    OrganizationCreateSerializer,
    ImageSerializer,
    CategoryListSerializerTest, CategoryListSerializer,
)


class OrganizationListAPIView(CreateModelMixin, ListAPIView):
    # permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    queryset = Account.objects.all()
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
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializers
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListCategory(mixins.CreateModelMixin, ListAPIView):
    permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = CategoryListSerializerTest
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = Category.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailCategory(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    RetrieveAPIView,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def put(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


