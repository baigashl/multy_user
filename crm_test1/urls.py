from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),

    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # api/password_reset/confirm/ - given token and new password

    path('api/account/', include('apps.accounts.urls')),
    path('api/review/', include('apps.reviews.urls')),
    path('api/gallery/', include('apps.gallery.urls')),
    path('api/account_owner/', include('apps.account_owner.urls')),
    path('accounts/', include('organizations.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
