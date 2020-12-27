from django.core.validators import validate_email
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignupSerializer, VerifyAccountSerializer
from .models import UserAccount
from django.shortcuts import get_object_or_404
import random
import requests


class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignupSerializer

    def post(self, request, format='json'):
        serializer = self.serializer_class(data=self.request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnverifiedAccountLoginView(APIView):
    serializer_class = VerifyAccountSerializer

    def get(self, request):
        user = UserAccount.objects.get(email__exact=self.request.user.email)
        user.phone = "0000000000"
        user.otp = "0000"
        verifyAccount = {
            "phone": user.phone,
            "otp": user.otp
        }
        serializer = self.serializer_class(instance=user, data=verifyAccount)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    serializer_class = VerifyAccountSerializer

    def get(self, request):
        user = UserAccount.objects.get(email__exact=self.request.user.email)
        serializer = self.serializer_class(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        if otp == "":
            phone_unique_check = UserAccount.objects.filter(
                phone__exact=phone).filter(is_verified=True).count()
            if phone_unique_check == 0:
                user = UserAccount.objects.get(
                    email__exact=self.request.user.email)
                user.phone = phone
                user.otp = str(random.randint(1000, 9999))
                otp = user.otp
                print(user.otp)
                verifyAccount = {
                    "phone": user.phone,
                    "otp": user.otp
                }
                serializer = self.serializer_class(
                    instance=user, data=verifyAccount)
                if serializer.is_valid():
                    user = serializer.save()
                    if user:
                        json = serializer.data

                        url_2factor = "https://2factor.in/API/V1/386516a5-c8f3-11ea-9fa5-0200cd936042/SMS/" + \
                            phone + "/" + otp + ""
                        response = requests.request("GET", url_2factor)
                        data = response.json()
                        if data['Status'] == "Error":
                            return Response({"detail": "Unable to send OTP. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)
                        # https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}
                        else:
                            return Response(json, status=status.HTTP_200_OK)

                        # return Response(json, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "User Account with this number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = UserAccount.objects.get(
                email__exact=self.request.user.email)
            if user.phone == phone:
                if user.otp == otp:
                    user.is_verified = True
                    verifyAccount = {
                        "is_verified": True,
                        "phone": user.phone,
                        "otp": user.otp
                    }
                    serializer = self.serializer_class(
                        instance=user, data=verifyAccount)
                    if serializer.is_valid():
                        user = serializer.save()
                        if user:
                            json = serializer.data
                            return Response(json, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "Entered OTP is invalid."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Phone numbers don't match."}, status=status.HTTP_400_BAD_REQUEST)
