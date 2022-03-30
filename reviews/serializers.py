from users.models import CustomUser
from rest_framework import serializers
from rest_framework.reverse import reverse

from reviews.models import Review
from users.serializers import UserAccountSerializer


class ReviewSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    user = UserAccountSerializer(read_only=True)
    nutrition = serializers.IntegerField(max_value=10, min_value=1)
    security = serializers.IntegerField(max_value=10, min_value=1)
    program = serializers.IntegerField(max_value=10, min_value=1)
    cleanliness = serializers.IntegerField(max_value=10, min_value=1)
    teacher = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = [
            'id',
            'url',
            'user',
            'account',
            'review',
            'nutrition',
            'security',
            'program',
            'cleanliness',
            'teacher',
            'rating_average',
        ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("detail-review", kwargs={"id": obj.id}, request=request)
