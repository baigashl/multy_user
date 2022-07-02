from django.contrib import admin
from .models import ReviewOffice, ReviewSchool, ReviewKindergarten

from .serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool


class MyModelAdminOffice(admin.ModelAdmin):
    serializer = CreateReviewOffice


class MyModelAdminSchool(admin.ModelAdmin):
    serializer = CreateReviewSchool


class MyModelAdminKindergarten(admin.ModelAdmin):
    serializer = CreateReviewKindergarten


admin.site.register(ReviewOffice, MyModelAdminOffice)
admin.site.register(ReviewSchool, MyModelAdminSchool)
admin.site.register(ReviewKindergarten, MyModelAdminKindergarten)
