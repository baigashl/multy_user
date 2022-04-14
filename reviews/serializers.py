from users.models import CustomUser
from rest_framework import serializers
from rest_framework.reverse import reverse

from reviews.models import ReviewSchool, ReviewOffice, ReviewKindergarten
from users.serializers import UserAccountSerializer


class CreateReviewSchool(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReviewSchool
        fields = [
            'id',
            'url',
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


class CreateReviewOffice(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReviewOffice
        fields = [
            'id',
            'url',
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


class CreateReviewKindergarten(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReviewKindergarten
        fields = [
            'id',
            'url',
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

