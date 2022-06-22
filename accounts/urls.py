from django.urls import path
from accounts.views import (
    AccountDetailAPIView,
    OrganizationListAPIView,
    OrganizationCreateAPIView,
    DetailCategory, ListCategory, AddRemoveWishListItemsView,
    OrganizationKindergartenListAPIView,
    OrganizationOfficeListAPIView,
    OrganizationSchoolListAPIView
)

urlpatterns = [
    path('', OrganizationListAPIView.as_view(), name='list-organization'),
    path('school/', OrganizationSchoolListAPIView.as_view(), name='school-list-organization'),
    path('kindergarten/', OrganizationKindergartenListAPIView.as_view(), name='kindergarten-list-organization'),
    path('office', OrganizationOfficeListAPIView.as_view(), name='office-list-organization'),
    path('add/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='detail-organization'),
    path('category/', ListCategory.as_view(), name='category'),
    path('category/<int:pk>/', DetailCategory.as_view(), name='detail_category'),

    # WishList add / remove item
    path('<int:id>/addwishlist/', AddRemoveWishListItemsView.as_view(), name='add-remove-wishlist'),
]
