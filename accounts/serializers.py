from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from accounts.models import Image, Account, Category
# from reviews.models import Review
# from reviews.serializers import ReviewSerializer
from reviews.serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool
from users.users_nested.serializers import OrganizationUserSerializer


class ImageSerializer(serializers.ModelSerializer):
    #max 50 images
    class Meta:
        model = Image
        fields = (
            # 'account_id',
            'images',
        )


class AccountDetailSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    review_office = CreateReviewOffice(many=True, read_only=True)
    review_school = CreateReviewSchool(many=True, read_only=True)
    review_cat_kindergarten = CreateReviewKindergarten(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            'user',
            'owner',
            'images',
            'review_office',
            'review_school',
            'review_cat_kindergarten'
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

    def get_images(self, obj):
        qs = Image.objects.filter(
            account_id=obj
        )
        return ImageSerializer(qs, many=True).data

    # def get_reviews(self, obj):
    #     qs = Review.objects.filter(
    #         account=obj
    #     )
    #     return ReviewSerializer(qs, many=True).data


class AccountSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    # images = ImageSerializer(many=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'url',
            'account_category',
            'name',
            'users',
            'owner',
            'images'
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

    def get_images(self, obj):
        qs = Image.objects.filter(
            account_id=obj
        )
        quantity = Image.objects.filter(
            account_id=obj
        ).count()
        imgs = []
        for i in range(quantity):
            imgs.append(ImageSerializer(qs, many=True).data[i]['images'])
        return imgs
        # return ImageSerializer(qs, many=True).data


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

    class Meta:
        model = Organization
        fields = ['name']
