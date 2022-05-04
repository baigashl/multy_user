from rest_framework import serializers
from rest_framework.reverse import reverse

from accounts.models import Account
from .models import (
    PostImg, GalleryImg,
    PostVideo, GalleryVideo
)
#  git stash
#  git pull origin master


#  Create


class CreateImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImg
        fields = [
            'gallery', 'image', 'gallery_id'
        ]

    def validate(self, attrs):
        if attrs['gallery_id'] != 1:
            raise serializers.ValidationError({"Gallery": "Full"})

        return attrs


class CreateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImg
        fields = [
            'gallery', 'image'
        ]

        # def validate(self, data):
        #     gallery_id = data.get('gallery_id', None)
        #     if PostImg.objects.values(gallery_id).count()<2:
        #         gallery_id = 0
        #     return data


class ListImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImg
        fields = [
            'gallery', 'video'
        ]


class CreateVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = '__all__'


class ListVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = '__all__'


#  Gallery


class GalleryImageSerializer(serializers.ModelSerializer):
    img = CreateImageSerializer(many=True, read_only=True)

    class Meta:
        model = GalleryImg
        fields = [
            'img'
        ]


class GalleryVideoSerializer(serializers.ModelSerializer):
    video = CreateVideoSerializer(many=True, read_only=True)

    class Meta:
        model = GalleryVideo
        fields = [
            'video'
        ]


class PostSerializer(serializers.ModelSerializer):
    gallery_img = GalleryImageSerializer(many=True, read_only=True)
    gallery_video = GalleryVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = [
            'name', 'gallery_img', 'gallery_video'
        ]


class PostSerializerList(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail_post", kwargs={"pk": obj.id}, request=request)

    class Meta:
        model = Account
        fields = [
            'name', 'url'
        ]
