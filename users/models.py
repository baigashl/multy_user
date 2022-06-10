from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    AbstractUser
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.dispatch import receiver
from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_account_owner = models.BooleanField(default=False)
    is_account_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

#
# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
#
#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )

