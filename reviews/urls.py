from django.urls import path

from reviews.views import (
    ListOffice,
    DetailOffice, ListSchool,
    DetailSchool, ListKindergarten,
    DetailKindergarten
)

urlpatterns = [
    # path('category/', ListCategory.as_view(), name='category'),
    # path('category/<int:pk>/', DetailCategory.as_view(), name='detail_category'),
    # path('post/', ListPost.as_view(), name='post'),
    # path('post/<int:pk>/', DetailPost.as_view(), name='detail_post'),
    path('office/', ListOffice.as_view(), name='office'),
    path('office/<int:id>/', DetailOffice.as_view(), name='detail_office'),
    path('school/', ListSchool.as_view(), name='school'),
    path('school/<int:id>/', DetailSchool.as_view(), name='detail_school'),
    path('kindergarten/', ListKindergarten.as_view(), name='kindergarten'),
    path('kindergarten/<int:id>/', DetailKindergarten.as_view(), name='detail_kindergarten'),
]
