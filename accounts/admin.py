from django.contrib import admin
from accounts.models import (
    Account, Image
)
admin.site.register(Account)
admin.site.register(Image)
