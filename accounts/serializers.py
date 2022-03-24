from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from accounts.models import Image, Account
from reviews.models import Review
from reviews.serializers import ReviewSerializer
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
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            'user',
            'owner',
            'images',
            'reviews'
        ]
        read_only_fields = ['id', 'user', 'owner', 'url']

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

    def get_reviews(self, obj):
        qs = Review.objects.filter(
            account=obj
        )
        return ReviewSerializer(qs, many=True).data



class AccountSerializers(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    # images = ImageSerializer(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'url',
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
        return ImageSerializer(qs, many=True).data


class OrganizationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['name']
