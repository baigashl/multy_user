from django.db import models
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationUser,
    AbstractOrganizationOwner
)
from organizations.models import (
    Organization,
    OrganizationUser
)

from users.models import CustomUser


class Account(Organization):
    pass


# class AccountUser(OrganizationUser):
#     account = models.ForeignKey(
#         Account,
#         # related_name='account_user',
#         on_delete=models.CASCADE
#     )
#     user = models.OneToOneField(
#         CustomUser,
#         on_delete=models.CASCADE
#     )
#
#     class Meta:
#         unique_together = ['account', 'user']
#
#
# class AccountOwner(AbstractOrganizationOwner):
#     account = models.OneToOneField(
#         Account,
#         related_name='account_owner',
#         on_delete=models.CASCADE
#     )
#     user = models.OneToOneField(
#         CustomUser,
#         on_delete=models.CASCADE
#     )
#
#     class Meta:
#         unique_together = ['account', 'user']



