from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from accounts.models import Image, Account, Category, Amenity
from gallery.models import PostImg, GalleryImg, GalleryVideo, PostVideo
from reviews.serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool
from users.users_nested.serializers import OrganizationUserSerializer
from gallery.serializers import GalleryVideoSerializer, GalleryImageSerializer


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
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


class WishListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'users_wishlist',
        ]


class AccountDetailSerializers(serializers.ModelSerializer):
    """
    organization only detail serializer
    """
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
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
            'users_wishlist'
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
        read_only_fields = ['owner', 'amenities']

    def create(self, validated_data):
        """
        add gallery image and video
        """
        # images = self.context['request'].FILES
        amenity = self.context['request'].data

        m1 = Account.objects.create(
            **validated_data
        )
        print(amenity.getlist("amenity"))
        if amenity.getlist("amenity"):
            for i in amenity.getlist("amenity"):
                amenityt_id = Amenity.objects.filter(slug=i).first()
                m1.amenities.add(amenityt_id.id)

        # gallery_of_account = GalleryImg.objects.create(
        #     post=m1
        # )
        # gallery_vid_of_account = GalleryVideo.objects.create(
        #     post=m1
        # )
        # account_image_model_instance = [
        #     PostImg(gallery=gallery_of_account, image=image) for image in images.getlist('images')
        # ]
        # account_video_model_instance = [
        #     PostVideo(gallery=gallery_vid_of_account, video=video) for video in images.getlist('videos')
        # ]
        # PostImg.objects.bulk_create(
        #     account_image_model_instance
        # )
        # PostVideo.objects.bulk_create(
        #     account_video_model_instance
        # )
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
