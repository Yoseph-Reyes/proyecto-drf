from django.urls import path, include
from .views import EmailVerificationView, Login, Registration, ChangePasswordView, ResendVerificationCode, ZurichRegister,ZurichLogin
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('register/', Registration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='login'),
    path('verify-token/', TokenVerifyView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('verify_email/', EmailVerificationView.as_view(), name="verify-email"),
    path('resend-ver-link/', ResendVerificationCode.as_view(), name="verify-email"),
]
 