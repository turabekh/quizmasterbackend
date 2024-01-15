from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileUpdateView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserProfileView,
)

urlpatterns = [
    # ... other URL patterns ...
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
