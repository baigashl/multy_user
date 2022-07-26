from django.db.models import Sum
from rest_framework import serializers
from rest_framework.reverse import reverse
from organizations.models import (
    OrganizationUser,
    Organization,
)
from apps.accounts.models import Image, Account, Category, Amenity, Price
from apps.gallery.models import PostImg, GalleryImg, GalleryVideo, PostVideo
from apps.reviews.models import ReviewSchool, ReviewOffice, ReviewKindergarten
from apps.reviews.serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool
from apps.users.users_nested.serializers import OrganizationUserSerializer
from apps.gallery.serializers import GalleryVideoSerializer, GalleryImageSerializer


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
            'phone',
            'instagram',
            'whatsapp',
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
            'users_wishlist',
            'paid',
            'check'
        ]
        read_only_fields = [
            'id',
            'user',
            'owner',
            'url',
            'users_wishlist',
            'paid',
            'check'
        ]

    # def get_or_create_amenity(self, amenities):
    #     amenity_ids = []
    #     for amenity in amenities:
    #         amenity_instance, created = Amenity.objects.get_or_create(
    #             pk=amenity.get('id'), defaults=amenity
    #         )
    #         amenity_ids.append(amenity_instance.pk)
    #     return amenity_ids
    def clear_existing_videos(self, instance, video_list):
        gallery = instance.gallery_video.first()
        videos = PostVideo.objects.filter(gallery=gallery).all()
        delete_videos = []
        for i in videos:
            if i.video.url in video_list:
                delete_videos.append(i)
        print(delete_videos)
        for post_video in delete_videos:
            print(post_video.video.url)
            # post_video.video.delete()
            post_video.delete()

    def clear_existing_images(self, instance, image_list):
        gallery = instance.gallery_img.first()
        images = PostImg.objects.filter(gallery=gallery).all()
        delete_images = []
        for i in images:
            if i.image.url in image_list:
                delete_images.append(i)

        for post_image in delete_images:
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
        image_list = data['gallery']

        if image_list:
            self.clear_existing_images(instance, image_list)

        if media.getlist('images'):
            print(media.getlist('images'))
            gallery_of_account = GalleryImg.objects.filter(
                post=instance
            ).first()
            account_image_model_instance = [
                PostImg(gallery=gallery_of_account, image=image) for image in
                media.getlist('images')
            ]
            PostImg.objects.bulk_create(
                account_image_model_instance
            )

        video_list = data['gallery_video'].split(',')

        if video_list:
            self.clear_existing_videos(instance, video_list)

        if media.getlist('videos'):
            gallery_vid_of_account = GalleryVideo.objects.filter(
                post=instance
            ).first()

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
            total_rating = format(total_rating / rating.count(), ".1f")

        return total_rating

    # def rating_object(self, instance):
    #     if instance.account_category.id == 1:
    #         rating = ReviewSchool.objects.filter(review_account=instance.id)
    #     if instance.account_category.id == 2:
    #         rating = ReviewKindergarten.objects.filter(review_account=instance.id)
    #     if instance.account_category.id == 3:
    #         rating = ReviewOffice.objects.filter(review_account=instance.id)

    def to_representation(self, instance):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

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
        wished = False
        if instance.users_wishlist.filter(id=user.id).exists():
            wished = True
        response['wished'] = wished
        if instance.account_category.id == 1:
            rating = ReviewSchool.objects.filter(review_account=instance.id)

            if rating:
                purity = format(rating.aggregate(Sum('purity'))['purity__sum'] / rating.count(), ".1f")
                nutrition = format(rating.aggregate(Sum('nutrition'))['nutrition__sum'] / rating.count(), ".1f")
                training_program = format(
                    rating.aggregate(Sum('training_program'))['training_program__sum'] / rating.count(), ".1f")
                security = format(rating.aggregate(Sum('security'))['security__sum'] / rating.count(), ".1f")
                locations = format(rating.aggregate(Sum('locations'))['locations__sum'] / rating.count(), ".1f")
                office = format(rating.aggregate(Sum('office'))['office__sum'] / rating.count(), ".1f")
                quality_of_education = format(
                    rating.aggregate(Sum('quality_of_education'))['quality_of_education__sum'] / rating.count(), ".1f")
                price_and_quality = format(
                    rating.aggregate(Sum('price_and_quality'))['price_and_quality__sum'] / rating.count(), ".1f")
                study_guides = format(rating.aggregate(Sum('study_guides'))['study_guides__sum'] / rating.count(),
                                      ".1f")
                response['avg_rating'] = [
                    {"name": "чистота", "rating": purity},
                    {"name": "питание", "rating": nutrition},
                    {"name": "программа обучения", "rating": training_program},
                    {"name": "безопасность", "rating": security},
                    {"name": "локации", "rating": locations},
                    {"name": "здание", "rating": office},
                    {"name": "качество образования", "rating": quality_of_education},
                    {"name": "соотнощение цена/качество", "rating": price_and_quality},
                    {"name": "учебные пособия", "rating": study_guides},
                ]

            else:
                response['avg_rating'] = [
                    {"name": "чистота", "rating": '0'},
                    {"name": "питание", "rating": '0'},
                    {"name": "программа обучения", "rating": '0'},
                    {"name": "безопасность", "rating": '0'},
                    {"name": "локации", "rating": '0'},
                    {"name": "здание", "rating": '0'},
                    {"name": "качество образования", "rating": '0'},
                    {"name": "соотнощение цена/качество", "rating": '0'},
                    {"name": "учебные пособия", "rating": '0'},
                ]


        if instance.account_category.id == 2:
            rating = ReviewKindergarten.objects.filter(review_account=instance.id)

            if rating:
                purity = format(rating.aggregate(Sum('purity'))['purity__sum'] / rating.count(), ".1f")
                nutrition = format(rating.aggregate(Sum('nutrition'))['nutrition__sum'] / rating.count(), ".1f")
                activity = format(rating.aggregate(Sum('activity'))['activity__sum'] / rating.count(), ".1f")
                upbringing = format(rating.aggregate(Sum('upbringing'))['upbringing__sum'] / rating.count(), ".1f")
                security = format(rating.aggregate(Sum('security'))['security__sum'] / rating.count(), ".1f")
                locations = format(rating.aggregate(Sum('locations'))['locations__sum'] / rating.count(), ".1f")
                office = format(rating.aggregate(Sum('office'))['office__sum'] / rating.count(), ".1f")
                baby_care = format(rating.aggregate(Sum('baby_care'))['baby_care__sum'] / rating.count(), ".1f")
                price_and_quality = format(
                    rating.aggregate(Sum('price_and_quality'))['price_and_quality__sum'] / rating.count(), ".1f")
                response['avg_rating'] = [
                    {"name": "чистота", "rating": purity},
                    {"name": "питание", "rating": nutrition},
                    {"name": "активность", "rating": activity},
                    {"name": "воспитание", "rating": upbringing},
                    {"name": "безопасность", "rating": security},
                    {"name": "локации", "rating": locations},
                    {"name": "архитектура", "rating": office},
                    {"name": "уход за ребенком", "rating": baby_care},
                    {"name": "соотнощение цена/качество", "rating": price_and_quality},
                ]
            else:
                response['avg_rating'] = [
                    {"name": "чистота", "rating": '0'},
                    {"name": "питание", "rating": '0'},
                    {"name": "активность", "rating": '0'},
                    {"name": "воспитание", "rating": '0'},
                    {"name": "безопасность", "rating": '0'},
                    {"name": "локации", "rating": '0'},
                    {"name": "архитектура", "rating": '0'},
                    {"name": "уход за ребенком", "rating": '0'},
                    {"name": "соотнощение цена/качество", "rating": '0'},
                ]


        if instance.account_category.id == 3:
            rating = ReviewOffice.objects.filter(review_account=instance.id)

            if rating:
                reputation = format(rating.aggregate(Sum('reputation'))['reputation__sum'] / rating.count(), ".1f")
                staff = format(rating.aggregate(Sum('staff'))['staff__sum'] / rating.count(), ".1f")
                support = format(rating.aggregate(Sum('support'))['support__sum'] / rating.count(), ".1f")
                accompany = format(rating.aggregate(Sum('accompany'))['accompany__sum'] / rating.count(), ".1f")
                efficiency = format(rating.aggregate(Sum('efficiency'))['efficiency__sum'] / rating.count(), ".1f")
                price_and_quality = format(
                    rating.aggregate(Sum('price_and_quality'))['price_and_quality__sum'] / rating.count(), ".1f")
                response['avg_rating'] = [
                    {"name": "репутация", "rating": reputation},
                    {"name": "персонал", "rating": staff},
                    {"name": "поддержка", "rating": support},
                    {"name": "сопровождение", "rating": accompany},
                    {"name": "эффективность", "rating": efficiency},
                    {"name": "соотнощение цена/качество", "rating": price_and_quality},
                ]
            else:
                response['avg_rating'] = [
                    {"name": "репутация", "rating": '0'},
                    {"name": "персонал", "rating": '0'},
                    {"name": "поддержка", "rating": '0'},
                    {"name": "сопровождение", "rating": '0'},
                    {"name": "эффективность", "rating": '0'},
                    {"name": "соотнощение цена/качество", "rating": '0'},
                ]

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
            'address',
            'phone',
            'lat',
            'lng',
            'price',
            'rating',
            'description',
            'users',
            'owner',
            'amenities',
            'gallery_img',
            'gallery_video',
            'paid',
            'check'
        ]
        read_only_fields = ['owner', 'amenities', 'rating', 'paid', 'check']

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
            total_rating = format(total_rating / rating.count(), ".1f")

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
