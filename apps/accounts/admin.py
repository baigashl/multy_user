from django.contrib import admin
from apps.accounts.models import (
    Account, Image, Category, Amenity
)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Image)
admin.site.register(Amenity)
