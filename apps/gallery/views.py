from rest_framework import mixins, generics, permissions, viewsets, status
from .serializers import (
    CreateImageSerializer, CreateVideoSerializer,
    GalleryImageSerializer, GalleryVideoSerializer,
    ListImageSerializer, ListVideoSerializer,
)
from .models import (
    PostImg, PostVideo,
    GalleryVideo, GalleryImg,
)


class ViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = PostImg.objects.all()
    serializer_class = CreateImageSerializer


class ListIMG(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    serializer_class = CreateImageSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = PostImg.objects.all()
        query = request.GET.get('id')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailIMG(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = PostImg.objects.all()
    serializer_class = CreateImageSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListVideo(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    serializer_class = CreateVideoSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = PostVideo.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)

class DetailVideo(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = PostVideo.objects.all()
    serializer_class = ListVideoSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListIMGGallery(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    serializer_class = GalleryImageSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = GalleryImg.objects.all()
        query = request.GET.get('id')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailImageGallery(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = GalleryImg.objects.all()
    serializer_class = GalleryImageSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ListVideoGallery(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = []
    serializer_class = GalleryVideoSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        qs = GalleryVideo.objects.all()
        query = request.GET.get('id')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class DetailVideoGallery(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView,
):
    permission_classes = []
    queryset = GalleryVideo.objects.all()
    serializer_class = GalleryVideoSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
