# yourapp/urls.py

from django.urls import path
from .views import UserPhoneNumberView, UserOTPValidationView

urlpatterns = [
    path('phone_number/', UserPhoneNumberView.as_view(), name='phone_number'),
    path('otp_validation/', UserOTPValidationView.as_view(), name='otp_validation'),
    # Add any other URLs as needed
]
