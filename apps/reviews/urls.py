from django.urls import path

from apps.reviews.views import (
    ListOffice,
    DetailOffice, ListSchool,
    DetailSchool, ListKindergarten,
    DetailKindergarten, DetailReview, ListReview
)

urlpatterns = [
    path('office/', ListOffice.as_view(), name='office'),
    path('office/<int:id>/', DetailOffice.as_view(), name='detail_office'),
    path('school/', ListSchool.as_view(), name='school'),
    path('school/<int:id>/', DetailSchool.as_view(), name='detail_school'),
    path('kindergarten/', ListKindergarten.as_view(), name='kindergarten'),
    path('kindergarten/<int:id>/', DetailKindergarten.as_view(), name='detail_kindergarten'),
    path('reviewtext/', ListReview.as_view(), name='review_list'),
    path('reviewtext/<int:id>/', DetailReview.as_view(), name='detail_review'),
]

