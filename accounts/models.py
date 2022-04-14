from django.db import models
from django.urls import reverse
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


class Category(models.Model):
    name_category = models.CharField(max_length=255)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_category

    def get_absolute_url(self):
        return reverse('detail_category', kwargs={'pk': self.pk})


class Account(Organization):
    account_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')
    description = models.TextField()
    deleted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)


class Image(models.Model):
    account_id = models.ForeignKey(
                    Account,
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



