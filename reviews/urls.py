from django.urls import path

from reviews.views import (
    ReviewListAPIView, ReviewDetailAPIView
)

urlpatterns = [
    path('', ReviewListAPIView.as_view(), name='list-review'),
    # path('add/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('<int:id>/', ReviewDetailAPIView.as_view(), name='detail-review'),
]
