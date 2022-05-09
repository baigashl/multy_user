from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from accounts.models import Image, Account, Category, Amenity
# from reviews.models import Review
# from reviews.serializers import ReviewSerializer
from gallery.models import PostImg, GalleryImg, GalleryVideo, PostVideo
from reviews.serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool
from users.users_nested.serializers import OrganizationUserSerializer
from gallery.serializers import GalleryVideoSerializer, GalleryImageSerializer


class ImageSerializer(serializers.ModelSerializer):
    #max 50 images
    class Meta:
        model = Image
        fields = (
            # 'account_id',
            'images',
        )


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (

            'name_category',
        )


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = (

            'name',
        )


class AccountDetailSerializers(serializers.ModelSerializer):
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    # account_category = serializers.CharField(source='account_category.name_category')
    user = serializers.SerializerMethodField(read_only=True)
    review_office = CreateReviewOffice(many=True, read_only=True)
    review_school = CreateReviewSchool(many=True, read_only=True)
    review_cat_kindergarten = CreateReviewKindergarten(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            'account_category',
            'user',
            'owner',
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


class AccountSerializers(serializers.ModelSerializer):
    """
    organization list and create serializer
    """
    url = serializers.SerializerMethodField(read_only=True)
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'url',
            'account_category',
            'name',
            'users',
            'owner',
            'amenities',
            'gallery_img',
            'gallery_video',
        ]
        read_only_fields = ['owner']

    def create(self, validated_data):
        images = self.context['request'].FILES
        m1 = Account.objects.create(
            **validated_data
        )
        account_image_model_instance = [
            Image(account_id=m1, images=image) for image in images.getlist('images')
        ]
        Image.objects.bulk_create(
            account_image_model_instance
        )
        return m1

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        amenity = response.pop("amenities")
        response['amenities'] = []
        for i in range(len(amenity)):
            response['amenities'].append(AmenitySerializer(instance.amenities.all(), many=True).data[i]['name'])
        response['account_category'] = CatSerializer(instance.account_category).data['name_category']
        return response


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


class CategoryListSerializer(serializers.ModelSerializer):
    url_category = serializers.SerializerMethodField(read_only=True)
    cat = AccountSerializers(many=True)

    class Meta:
        model = Category
        fields = [
            'name_category',
            'update',
            'timestamp',
            'url_category',
            'cat'
        ]

    def get_url_category(self, obj):
        return reverse('detail_category', kwargs={'pk': obj.id})


class CategoryListSerializerTest(serializers.ModelSerializer):
    url_category = serializers.SerializerMethodField(read_only=True)

    def get_url_category(self, obj):
        return reverse('detail_category', kwargs={'pk': obj.id})

    class Meta:
        model = Category
        fields = [
            'name_category',
            'update',
            'timestamp',
            'url_category',
        ]


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """
    organization create serializer
    """
    class Meta:
        model = Organization
        fields = ['name']
