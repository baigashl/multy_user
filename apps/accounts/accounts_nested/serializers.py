from organizations.models import Organization, OrganizationUser
from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.accounts.models import Account, Price
from apps.accounts.serializers import AmenitySerializer, CatSerializer, PriceSerializer
from apps.gallery.models import GalleryImg, PostImg, GalleryVideo, PostVideo
from apps.gallery.serializers import GalleryImageSerializer, GalleryVideoSerializer
from apps.reviews.models import ReviewSchool, ReviewKindergarten, ReviewOffice
from apps.reviews.serializers import (
    CreateReviewOffice, CreateReviewSchool, CreateReviewKindergarten
)
from apps.users.users_nested.serializers import OrganizationUserSerializer


class AccountInlineSerializers(serializers.ModelSerializer):
    """
    organization only detail serializer
    """
    # current_user = serializers.SerializerMethodField()
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)
    review_office = CreateReviewOffice(many=True, read_only=True)
    review_school = CreateReviewSchool(many=True, read_only=True)
    review_cat_kindergarten = CreateReviewKindergarten(many=True, read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            'price',
            'description',
            'rating',
            'account_category',
            'gallery_img',
            'gallery_video',
            'amenities',
            'review_office',
            'review_school',
            'review_cat_kindergarten',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)

    def get_user(self, obj):
        qs = OrganizationUser.objects.filter(
            organization=obj
        )
        return OrganizationUserSerializer(qs, many=True).data

    def get_price(self, obj):
        price = Price.objects.filter(account=obj).first()
        return PriceSerializer(price).data

    def get_rating(self, obj):
        rating = []
        if obj.account_category.id == 1:
            rating = ReviewSchool.objects.filter(review_account=obj.id)
        if obj.account_category.id == 2:
            rating = ReviewKindergarten.objects.filter(review_account=obj.id)
        if obj.account_category.id == 3:
            rating = ReviewOffice.objects.filter(review_account=obj.id)
        total_rating = 0

        if rating:
            for rate in rating:
                total_rating += rate.rating_average()
            total_rating = format(total_rating/rating.count(), ".1f")
        return total_rating

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

        user = self.context.get('current_user')

        response = super().to_representation(instance)
        amenity = response.pop("amenities")
        response['amenities'] = []
        for i in range(len(amenity)):
            response['amenities'].append(AmenitySerializer(instance.amenities.all(), many=True).data[i]['name'])
        response['account_category'] = CatSerializer(instance.account_category).data['name_category']
        wished = False

        if instance.users_wishlist.filter(id=user.id).exists():
            wished = True
        response['wished'] = wished
        return response