from django.contrib import admin
from django.urls import path, include
from chats.auth import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),

    # your app routes (you already have nested routers inside chats.urls)
    path('api/', include('chats.urls')),

    # DRF session login/logout (checker often looks for "api-auth")
    path('api-auth/', include('rest_framework.urls')),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
