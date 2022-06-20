from firebase_admin import auth
from organizations.models import OrganizationUser
from rest_framework.generics import (
    RetrieveAPIView, ListAPIView, ListCreateAPIView
)
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    UserDetailSerializer,
    UserAccountSerializer, RegisterOrgUserSerializers, OrgUserDetailSerializer, UserWishListSerializer
)
from rest_framework import status


class RegisterUser(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = CustomUser.objects.get(uid=request.user.uid)
        firebase_data = auth.get_user(user.email)
        user.email = firebase_data.email
        user.save()
        return Response({'message': 'User Registered'})


class OrgUserListApiView(ListCreateAPIView):
    permission_classes = []
    serializer_class = RegisterOrgUserSerializers
    queryset = OrganizationUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = RegisterOrgUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    permission_classes = []

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserWishListAPIView(RetrieveAPIView):
    """
    wish list view
    """
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserWishListSerializer
    permission_classes = []
    lookup_field = 'email'


class UserListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = UserAccountSerializer
    # search_fields = ('user__username', 'content')
    queryset = CustomUser.objects.all()


class OrgUserDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrgUserDetailSerializer
    permission_classes = []

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
