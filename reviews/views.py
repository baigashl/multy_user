from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewListAPIView(CreateModelMixin, ListAPIView):
    # permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = ReviewSerializer
    # search_fields = ('user__username', 'content')
    queryset = Review.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        old_obj = self.request.data
        # org = serializer.save()
        user = self.request.user

        serializer.save(user=user)


class ReviewDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
    permission_classes = []
    authentication_classes = [SessionAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


