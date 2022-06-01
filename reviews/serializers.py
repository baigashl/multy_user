from accounts.models import Account
from rest_framework import serializers
from rest_framework.reverse import reverse

from reviews.models import ReviewSchool, ReviewOffice, ReviewKindergarten
from users.users_nested.serializers import UserPublicSerializer


class CreateReviewSchool(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    review_user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ReviewSchool
        fields = [
            'id',
            'url',
            'timestamp',
            'review_user',
            'review_account', 'review',
            'purity', 'nutrition', 'training_program',
            'security', 'locations', 'office', 'quality_of_education',
            'price_and_quality', 'study_guides', 'rating_average',
        ]
        read_only_fields = [
            'id',
            'url',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail_school", kwargs={"id": obj.id}, request=request)

    def __init__(self, *args, **kwargs):
        super(CreateReviewSchool, self).__init__(*args, **kwargs)
        self.fields['review_account'].queryset = Account.objects.filter(account_category__name_category='school')


class CreateReviewOffice(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    review_user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ReviewOffice
        fields = [
            'id',
            'url',
            'timestamp',
            'review_user',
            'review_account', 'review',
            'reputation', 'staff', 'support', 'accompany',
            'efficiency', 'price_and_quality', 'rating_average'
        ]
        read_only_fields = [
            'id',
            'url',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail_office", kwargs={"id": obj.id}, request=request)


    def __init__(self, *args, **kwargs):
        super(CreateReviewOffice, self).__init__(*args, **kwargs)
        self.fields['review_account'].queryset = Account.objects.filter(account_category__name_category='office')


class CreateReviewKindergarten(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    review_user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ReviewKindergarten
        fields = [
            'id',
            'url',
            'timestamp',
            'review_user',
            'review_account', 'review',
            'purity', 'nutrition', 'activity', 'upbringing',
            'security', 'locations', 'office', 'baby_care',
            'price_and_quality', 'rating_average'
        ]
        read_only_fields = [
            'id',
            'url',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail_kindergarten", kwargs={"id": obj.id}, request=request)

    def __init__(self, *args, **kwargs):
        super(CreateReviewKindergarten, self).__init__(*args, **kwargs)
        self.fields['review_account'].queryset = Account.objects.filter(account_category__name_category='kindergarten')

