from django.urls import path

from apps.account_owner.views import (
    AccountOrganizationOwnerView
)

urlpatterns = [
    path('', AccountOrganizationOwnerView.as_view(), name='org-owner-list'),
]
