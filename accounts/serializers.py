from django.db.models import Sum
from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from accounts.models import Image, Account, Category, Amenity, Price
from gallery.models import PostImg, GalleryImg, GalleryVideo, PostVideo
from reviews.models import ReviewSchool, ReviewOffice, ReviewKindergarten
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
            'slug'
        )


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = [
            'price',
            'extra_price',
            'month_price',
            'month_extra_price'
        ]



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
    rating = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'url',
            'id',
            'name',
            'address',
            'description',
            'lat',
            'lng',
            'price',
            'rating',
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

    # def get_or_create_amenity(self, amenities):
    #     amenity_ids = []
    #     for amenity in amenities:
    #         amenity_instance, created = Amenity.objects.get_or_create(
    #             pk=amenity.get('id'), defaults=amenity
    #         )
    #         amenity_ids.append(amenity_instance.pk)
    #     return amenity_ids
    def clear_existing_videos(self, instance):
        gallery = instance.gallery_video.first()
        videos = PostVideo.objects.filter(gallery=gallery).all()
        for post_video in videos:
            post_video.video.delete()
            post_video.delete()

    def clear_existing_images(self, instance):
        gallery = instance.gallery_img.first()
        images = PostImg.objects.filter(gallery=gallery).all()
        for post_image in images:
            post_image.image.delete()
            post_image.delete()

    def create_or_update_amenity(self, amenities):
        amenity_ids = []
        for amenity in amenities:
            amenity_instance, created = Amenity.objects.update_or_create(
                pk=amenity.id)
            amenity_ids.append(amenity_instance.pk)
        return amenity_ids

    # def create_or_update_price(self, instance):
    #     price = instance.price.first()
    #
    #     return amenity_ids

    def update(self, instance, validated_data):
        """

        """
        price = Price.objects.get(
            account=instance
        )
        amenity = []
        data = self.context['request'].data
        media = self.context['request'].FILES
        print(data['price'])
        price.price = data['price'] if data['price'] else price.price
        price.extra_price = data['extra_price'] if data['extra_price'] else price.extra_price
        price.moth_price = data['month_price'] if data['month_price'] else price.month_price
        price.month_extra_price = data['month_extra_price'] if data['month_extra_price'] else price.month_extra_price
        price.save()
        if data.getlist("amenity"):
            for i in data.getlist("amenity"):
                amenity_id = Amenity.objects.filter(slug=i).first()
                amenity.append(amenity_id)
        instance.amenities.set(self.create_or_update_amenity(amenity))

        if media.getlist('images'):
            self.clear_existing_images(instance)
            gallery_of_account = GalleryImg.objects.filter(
                post=instance
            ).first()
            # print(gallery_of_account)
            account_image_model_instance = [
                PostImg(gallery=gallery_of_account, image=image) for image in
                media.getlist('images')
            ]
            PostImg.objects.bulk_create(
                account_image_model_instance
            )

        if media.getlist('videos'):
            self.clear_existing_videos(instance)
            gallery_vid_of_account = GalleryVideo.objects.filter(
                post=instance
            ).first()
            # print(gallery_of_account)
            account_video_model_instance = [
                PostVideo(gallery=gallery_vid_of_account, video=video) for
                video in media.getlist('videos')
            ]
            PostVideo.objects.bulk_create(
                account_video_model_instance
            )

        fields = [
            'name',
            'account_category',
            'address',
            'description',
            'lat',
            'lng',

        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        return instance

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)

    def get_price(self, obj):
        price = Price.objects.filter(account=obj).first()
        return PriceSerializer(price).data

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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        amenity = response.pop("amenities")
        response['amenities'] = []
        for i in range(len(amenity)):
            response['amenities'].append(
                {
                    'name': AmenitySerializer(instance.amenities.all(), many=True).data[i]['name'],
                    'icon': AmenitySerializer(instance.amenities.all(), many=True).data[i]['slug']
                }
            )
        response['account_category'] = CatSerializer(instance.account_category).data['name_category']
        return response


class AccountSerializers(serializers.ModelSerializer):
    """
    organization list and create serializer
    """
    url = serializers.SerializerMethodField(read_only=True)
    gallery_img = serializers.SerializerMethodField(read_only=True)
    gallery_video = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'url',
            'account_category',
            'name',
            'price',
            'rating',
            'description',
            'users',
            'owner',
            'amenities',
            'gallery_img',
            'gallery_video',
        ]
        read_only_fields = ['owner', 'amenities', 'rating']

    def create(self, validated_data):
        """
        add gallery image and video
        """
        # images = self.context['request'].FILES
        amenity = self.context['request'].data

        m1 = Account.objects.create(
            **validated_data
        )
        if amenity.getlist("amenity"):
            for i in amenity.getlist("amenity"):
                amenityt_id = Amenity.objects.filter(slug=i).first()
                m1.amenities.add(amenityt_id.id)

        return m1

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-organization", kwargs={"id": obj.id}, request=request)


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

    def to_representation(self, instance):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

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
