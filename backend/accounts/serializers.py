from rest_framework import serializers
from .models import UserAccount
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = UserAccount
        fields = ['email', 'name',
                  'user_type', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        user_type = attrs.get('user_type', '')

        if not re.match(r"^[a-zA-Z ]*$", name):
            raise serializers.ValidationError(
                {'name': 'name must only contain alphabets.'})
        # if User.objects.filter(phone=phone).exists():
        #     raise serializers.ValidationError(
        #         {'phone': "user account with this number already exists."})
        # if not phone.isdigit():
        #     raise serializers.ValidationError(
        #         {'phone': 'phone number must only contain digits.'})
        return attrs

    def create(self, validated_data):
        return UserAccount.objects.create_user(**validated_data)


class VerifyAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['phone', 'otp', 'is_verified']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        otp = attrs.get('otp', '')
        # is_verified = attrs.get('is_verified', '')

        if not phone.isdigit():
            raise serializers.ValidationError(
                {'phone': 'phone number should only contain digits.'})
        if len(phone) != 10:
            raise serializers.ValidationError(
                {'phone': 'phone number must be 10 digits.'})
        return attrs
