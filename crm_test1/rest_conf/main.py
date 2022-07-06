
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        #  'rest_framework_simplejwt.authentication.JWTAuthentication',

        # Main Firebase auth system
        'apps.users.authentication.FirebaseAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DATETIME_FORMAT': "%d %b, %Y",
}




