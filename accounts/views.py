from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView, ListAPIView, CreateAPIView
)
from rest_framework.mixins import (
    UpdateModelMixin,
    DestroyModelMixin, CreateModelMixin,
)
from organizations.models import (
    Organization, OrganizationOwner
)
from rest_framework.response import Response

from accounts.serializers import (
    AccountDetailSerializers,
    AccountSerializers, OrganizationCreateSerializer,
)


class OrganizationListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    queryset = Organization.objects.all()

    # def post(self, request, *args, **kwargs):
    #     serializer = OrganizationCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationCreateAPIView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Organization.objects.all()
    serializer_class = OrganizationCreateSerializer


class AccountDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    permission_classes = []
    # authentication_classes = []
    queryset = Organization.objects.all()
    serializer_class = AccountDetailSerializers
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


