from django.urls import path
# )

from apps.users.views import (
    UserDetailAPIView,
    UserListAPIView, OrgUserListApiView,
    OrgUserDetailAPIView, UserWishListAPIView, RegisterUser,
)

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('orguser/', OrgUserListApiView.as_view(), name='org_user-list'),
    path('orguser/<int:pk>', OrgUserDetailAPIView.as_view(), name='org_user-detail'),

    # Wishlist display
    path('<email>/wishlist/', UserWishListAPIView.as_view(), name='wishlist'),

    # path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='auth_register'),
]