from django.contrib import admin
from .models import ReviewOffice, ReviewSchool, ReviewKindergarten, ReviewText

from .serializers import CreateReviewOffice, CreateReviewKindergarten, CreateReviewSchool, ReviewSerializer


class MyModelAdminOffice(admin.ModelAdmin):
    serializer = CreateReviewOffice


class MyModelAdminSchool(admin.ModelAdmin):
    serializer = CreateReviewSchool


class MyModelAdminKindergarten(admin.ModelAdmin):
    serializer = CreateReviewKindergarten


class MyModelAdminReview(admin.ModelAdmin):
    serializer = ReviewSerializer


admin.site.register(ReviewOffice, MyModelAdminOffice)
admin.site.register(ReviewSchool, MyModelAdminSchool)
admin.site.register(ReviewKindergarten, MyModelAdminKindergarten)
admin.site.register(ReviewText, MyModelAdminReview)

