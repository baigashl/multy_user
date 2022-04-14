from django.contrib import admin
from accounts.models import (
    Account, Image, Category
)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Image)
