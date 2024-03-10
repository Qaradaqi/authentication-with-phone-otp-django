# yourapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserPhoneNumberSerializer, UserOTPValidationSerializer
from .models import CustomUser
import pyotp
from datetime import datetime


class UserPhoneNumberView(APIView):
    def post(self, request):
        serializer = UserPhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                # If the user is not registered, create a new user
                user = CustomUser.objects.create_user(phone_number=phone_number)

            # Ensure the OTP secret is not None
            if user.otp_secret is None:
                user.otp_secret = pyotp.random_base32()
                user.save()

            # Generate a new OTP for each login attempt
            otp = self.generate_otp(user)
            print(otp)

            # Send the OTP to the user (e.g., using a third-party service)
            # Note: This step is not implemented here and should be adapted based on your SMS service or other communication method.

            # Set the OTP and OTP creation time
            user.otp_created_at = datetime.now()
            user.save()

            return Response(
                {"message": "OTP sent successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_otp(self, user):
        # Ensure the OTP secret is not None
        if user.otp_secret is not None:
            # Use the user's OTP secret to generate a new OTP
            totp = pyotp.TOTP(user.otp_secret, interval=120)
            return totp.now()

        return None


class UserOTPValidationView(APIView):
    def post(self, request):
        serializer = UserOTPValidationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp = serializer.validated_data["otp"]

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Verify the received OTP
            if self.verify_otp(user, otp):
                # Clear the OTP fields after successful login
                user.otp_created_at = None
                user.save()

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response(
                    {"refresh": str(refresh), "access_token": access_token},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_otp(self, user, otp):
        # Verify the OTP using the user's OTP secret
        totp = pyotp.TOTP(user.otp_secret, interval=120)
        return totp.verify(otp)
