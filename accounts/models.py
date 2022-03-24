from django.db import models
from django.utils.translation import gettext_lazy as _
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


def upload_path(instance, filename):
    return 'account/{image_name}'.format(
        image_name=filename
    )


class Account(Organization):
    description = models.TextField()
    deleted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)


class Image(models.Model):
    account_id = models.ForeignKey(
                    Organization,
                    on_delete=models.CASCADE
                )
    images = models.ImageField(upload_to=upload_path, null=True, blank=True)


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



