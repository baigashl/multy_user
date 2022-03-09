from django.urls import path

from accounts.views import (
    AccountDetailAPIView,
    OrganizationListAPIView, OrganizationCreateAPIView,
)
urlpatterns = [
    path('', OrganizationListAPIView.as_view(), name='list-organization'),
    path('add/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('<int:id>/', AccountDetailAPIView.as_view(), name='detail-organization'),
]