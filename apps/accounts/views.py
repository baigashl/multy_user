from django.contrib.messages.storage import session
from rest_framework import mixins, status, permissions
from rest_framework.generics import (
    RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
)
from rest_framework.mixins import (
    UpdateModelMixin,
    DestroyModelMixin, CreateModelMixin,
)
from organizations.models import (
    Organization, OrganizationOwner, OrganizationUser
)

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Category, Account, Price
from apps.accounts.serializers import (
    AccountDetailSerializers,
    AccountSerializers,
    OrganizationCreateSerializer,
    ImageSerializer,
    CategoryListSerializerTest, CategoryListSerializer, WishListSerializers,
)
from apps.gallery.models import GalleryImg, GalleryVideo, PostImg, PostVideo


class OrganizationFeaturedListAPIView(ListAPIView):
    """
    Organization office list/create view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    # queryset = Account.objects.filter(featured=True, check=True).all()
    # lookup_field = 'id'

    def get_queryset(self):
        request = self.request
        qs = Account.objects.filter(check=True).all().order_by('-featured')
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs


class OrganizationOfficeListAPIView(ListAPIView):
    """
    Organization office list/create view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    # queryset = Account.objects.filter(account_category=3, check=True).all()
    # lookup_field = 'id'

    def get_queryset(self):
        request = self.request
        qs = Account.objects.filter(account_category=3, check=True).all().order_by('-featured')
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs


class OrganizationKindergartenListAPIView(ListAPIView):
    """
    Organization office list/create view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    # queryset = Account.objects.filter(account_category=2, check=True).all()
    # lookup_field = 'id'

    def get_queryset(self):
        request = self.request
        qs = Account.objects.filter(account_category=2, check=True).all().order_by('-featured')
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        print(query)
        return qs


class OrganizationSchoolListAPIView(ListAPIView):
    """
    Organization office list/create view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    # queryset = Account.objects.filter(account_category=1, check=True).all().order_by('-featured')
    lookup_field = 'id'

    def get_queryset(self):
        request = self.request
        qs = Account.objects.filter(account_category=1, check=True).all().order_by('-featured')
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs


class OrganizationAllListAPIView(ListAPIView):
    """
    Organization list view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializers
    queryset = Account.objects.filter(check=True).all()
    lookup_field = 'id'


class OrganizationListAPIView(CreateModelMixin, ListAPIView):
    """
    Organization list/create view
    """
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = []
    serializer_class = AccountSerializers
    # search_fields = ('user__username', 'content')
    queryset = Account.objects.filter(check=True).all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        org = serializer.save()
        user = self.request.user
        media = self.request.FILES
        data = self.request.data
        price = Price.objects.create(
            account=org,
            price=float(data['price']) if data['price'] else 0,
            extra_price=float(data['extra_price']) if data['extra_price'] else 0,
            month_price=float(data['month_price']) if data['month_price'] else 0,
            month_extra_price=float(data['month_extra_price']) if data['month_extra_price'] else 0,
        )
        org_user = OrganizationUser.objects.create(
            user=user,
            organization=org
        )
        org_owner = OrganizationOwner.objects.create(
            organization_user=org_user,
            organization=org
        )

        gallery_of_account = GalleryImg.objects.create(
            post=org
        )
        gallery_vid_of_account = GalleryVideo.objects.create(
            post=org
        )

        account_image_model_instance = [
            PostImg(gallery=gallery_of_account, image=image) for image in media.getlist('images')
        ]
        account_video_model_instance = [
            PostVideo(gallery=gallery_vid_of_account, video=video) for video in media.getlist('videos')
        ]
        PostImg.objects.bulk_create(
            account_image_model_instance
        )
        PostVideo.objects.bulk_create(
            account_video_model_instance
        )

        serializer.save(organization_user=org_user, organization_owner=org_owner)


class AccountDetailAPIView(RetrieveAPIView):
    """
    Organization detail/update/delete view
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializers
    lookup_field = 'id'


class AccountDetailAPIViewUpdate(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    """
    Organization detail/update/delete view
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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


class AddRemoveWishListItemsView(UpdateAPIView):
    permission_classes = []
    queryset = Account.objects.all()
    serializer_class = WishListSerializers
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            # print(instance.users_wishlist.filter(id=user.id).exists())
            account = serializer.save()
            if account.users_wishlist.filter(id=user.id).exists():
                account.users_wishlist.remove(user)
            else:
                account.users_wishlist.add(user)
            # print(instance.users_wishlist.filter(id=user.id).exists())
            return Response({"message": "wishlist updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})
