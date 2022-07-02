from django.contrib import admin
from django.urls import path
from .views import (
    ListIMG, ListVideo,
    ListIMGGallery, ListVideoGallery,
    DetailIMG, DetailVideo,
    DetailVideoGallery, DetailImageGallery
)

urlpatterns = [
    # path('post/', ListPost.as_view(), name='post'),
    # path('post/<int:pk>/', DetailPost.as_view(), name='detail_post'),
    path('create/img/', ListIMG.as_view(), name='create_img'),
    path('create/img/<int:pk>/', DetailIMG.as_view(), name='detail_img'),
    path('create/video/', ListVideo.as_view(), name='create_video'),
    path('create/video/<int:pk>/', DetailVideo.as_view(), name='detail_video'),
    path('gallery/img/', ListIMGGallery.as_view(), name='gallery_img'),
    path('gallery/video', ListVideoGallery.as_view(), name='gallery_video'),
    path('gallery/video/<int:pk>/', DetailVideoGallery.as_view(), name='gallery_img'),
    path('gallery/img/<int:pk>/', DetailImageGallery.as_view(), name='gallery_img'),
]