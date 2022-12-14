from django.urls import path
from apps.accounts.views import (
    AccountDetailAPIView,
    OrganizationListAPIView,
    DetailCategory, ListCategory, AddRemoveWishListItemsView,
    OrganizationKindergartenListAPIView,
    OrganizationOfficeListAPIView,
    OrganizationSchoolListAPIView,
    OrganizationFeaturedListAPIView,
    OrganizationAllListAPIView,
    AccountDetailAPIViewUpdate,
)

urlpatterns = [
    path('', OrganizationAllListAPIView.as_view(), name='list-organization'),
    path('create/', OrganizationListAPIView.as_view(), name='create-organization'),
    path('featured/', OrganizationFeaturedListAPIView.as_view(), name='featured-list-organization'),
    path('school/', OrganizationSchoolListAPIView.as_view(), name='school-list-organization'),
    path('kindergarten/', OrganizationKindergartenListAPIView.as_view(), name='kindergarten-list-organization'),
    path('office/', OrganizationOfficeListAPIView.as_view(), name='office-list-organization'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='detail-organization'),
    path('category/', ListCategory.as_view(), name='category'),
    path('category/<int:pk>/', DetailCategory.as_view(), name='detail_category'),
    path('update/<int:id>/', AccountDetailAPIViewUpdate.as_view(), name='detail-organization-update'),
    # WishList add / remove item
    path('<int:id>/addwishlist/', AddRemoveWishListItemsView.as_view(), name='add-remove-wishlist'),
]
