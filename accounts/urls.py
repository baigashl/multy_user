from django.urls import path
from accounts.views import (
    AccountDetailAPIView,
    OrganizationListAPIView,
    OrganizationCreateAPIView,
    DetailCategory, ListCategory,
)
urlpatterns = [
    path('', OrganizationListAPIView.as_view(), name='list-organization'),
    path('add/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='detail-organization'),
    path('category/', ListCategory.as_view(), name='category'),
    path('category/<int:pk>/', DetailCategory.as_view(), name='detail_category'),
]

"""
Api for organisation 

"""
