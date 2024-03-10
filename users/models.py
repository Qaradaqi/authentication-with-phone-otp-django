# yourapp/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import pyotp
from datetime import datetime, timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if phone_number is None or len(str(phone_number)) == 0:
            raise ValueError('The phone number field must be set')

        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)

        # Generate OTP secret
        user.otp_secret = pyotp.random_base32()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if phone_number is None or len(str(phone_number)) == 0:
            raise ValueError('The phone number field must be set for superuser')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    phone_number = PhoneNumberField(unique=True)
    otp_secret = models.CharField(max_length=16, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_validity_duration = models.DurationField(default=timedelta(minutes=2))

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
