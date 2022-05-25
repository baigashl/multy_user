from django.urls import path
from accounts.views import (
    AccountDetailAPIView,
    OrganizationListAPIView,
    OrganizationCreateAPIView,
    DetailCategory, ListCategory, AddRemoveWishListItemsView,
)
urlpatterns = [
    path('', OrganizationListAPIView.as_view(), name='list-organization'),
    path('add/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='detail-organization'),
    path('category/', ListCategory.as_view(), name='category'),
    path('category/<int:pk>/', DetailCategory.as_view(), name='detail_category'),

    # WishList add / remove item
    path('addwishlist/<int:id>/', AddRemoveWishListItemsView.as_view(), name='add-remove-wishlist'),
]
