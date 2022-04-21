from rest_framework import mixins, generics
from rest_framework.generics import ListAPIView

# from reviews.models import Review
# from reviews.serializers import ReviewSerializer


# class ReviewListAPIView(CreateModelMixin, ListAPIView):
#     # permission_classes = []
#     # authentication_classes = [SessionAuthentication]
#     serializer_class = ReviewSerializer
#     # search_fields = ('user__username', 'content')
#     queryset = Review.objects.all()
#     lookup_field = 'id'
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         old_obj = self.request.data
#         # org = serializer.save()
#         user = self.request.user
#
#         serializer.save(user=user)
#
#
# class ReviewDetailAPIView(UpdateModelMixin, DestroyModelMixin, RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = [SessionAuthentication]
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     lookup_field = 'id'
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
from reviews.models import ReviewSchool, ReviewOffice, ReviewKindergarten
from reviews.serializers import CreateReviewSchool, CreateReviewOffice, CreateReviewKindergarten


class ListOffice(mixins.CreateModelMixin, ListAPIView):
    permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = CreateReviewOffice
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = ReviewOffice.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailOffice(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = ReviewOffice.objects.all()
    serializer_class = CreateReviewOffice
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListSchool(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = CreateReviewSchool
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = ReviewSchool.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailSchool(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = ReviewSchool.objects.all()
    serializer_class = CreateReviewSchool
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ListKindergarten(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    # authentication_classes = [SessionAuthentication]
    serializer_class = CreateReviewKindergarten
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = ReviewKindergarten.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailKindergarten(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = ReviewKindergarten.objects.all()
    serializer_class = CreateReviewKindergarten
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



