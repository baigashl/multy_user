from organizations.models import Organization, OrganizationUser
from rest_framework import serializers
from rest_framework.reverse import reverse

from accounts.models import Account
from accounts.serializers import AmenitySerializer, CatSerializer
from gallery.models import GalleryImg, PostImg, GalleryVideo, PostVideo
from gallery.serializers import GalleryImageSerializer, GalleryVideoSerializer
from reviews.serializers import (
    CreateReviewOffice, CreateReviewSchool, CreateReviewKindergarten
)
from users.users_nested.serializers import OrganizationUserSerializer


class AccountInlineSerializers(serializers.ModelSerializer):
    """
        organization only detail serializer
        """
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    # user = serializers.SerializerMethodField(read_only=True)
    review_office = CreateReviewOffice(many=True, read_only=True)
    review_school = CreateReviewSchool(many=True, read_only=True)
    review_cat_kindergarten = CreateReviewKindergarten(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            # 'account_category',
            'review_office',
            'review_school',
            'review_cat_kindergarten',
            'gallery_img',
            'gallery_video',
            'amenities',
        ]
        read_only_fields = [
            'id',
            'user',
            'owner',
            'url',
            'users_wishlist'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)

    def get_user(self, obj):
        qs = OrganizationUser.objects.filter(
            organization=obj
        )
        return OrganizationUserSerializer(qs, many=True).data

    def get_gallery_img(self, obj):
        gallery_qs = GalleryImg.objects.filter(post=obj).all()
        gallery_count = PostImg.objects.filter(gallery=gallery_qs.first()).count()

        imgs = []
        for i in range(gallery_count):
            imgs.append(GalleryImageSerializer(gallery_qs, many=True).data[0]['img'][i]['image'])
        return imgs

    def get_gallery_video(self, obj):
        gallery_qs = GalleryVideo.objects.filter(post=obj).all()
        gallery_count = PostVideo.objects.filter(gallery=gallery_qs.first()).count()

        vids = []

        for i in range(gallery_count):
            vids.append(GalleryVideoSerializer(gallery_qs, many=True).data[0]['video'][i]['video'])
        return vids

    def to_representation(self, instance):
        response = super().to_representation(instance)
        amenity = response.pop("amenities")
        response['amenities'] = []
        for i in range(len(amenity)):
            response['amenities'].append(AmenitySerializer(instance.amenities.all(), many=True).data[i]['name'])
        response['account_category'] = CatSerializer(instance.account_category).data['name_category']
        return response