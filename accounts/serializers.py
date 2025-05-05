from rest_framework import serializers
from .models import OTP, CustomUser, ProfileUser, OTPRequest
from django.utils import timezone


class PhoneNumberSerializers(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("phone number must be digits")
        return value


class VerifyOTPSerializers(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        phone = data['phone_number']
        code = data['code']
        try:
            user = CustomUser.objects.get(phone_number=phone)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User DoesNotExist")
        otp_opj = OTP.objects.filter(user=user, code=code, is_verified=False).last()
        if not otp_opj:
            raise serializers.ValidationError("Invalid or expired code.")

        if otp_opj.is_expired():
            raise serializers.ValidationError("Code has expired")

        otp_opj.is_verified = True
        otp_opj.save()
        data['user'] = user
        return data


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['id', 'name', 'last_name', 'id_code', 'address', 'avatar', 'created_at', 'updated_at']


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'code', 'created_at', 'expires_at', 'is_verified']


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileUserSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'profile']


class OTPRequestSerializer(serializers.ModelSerializer):
    otp = OTPSerializer(read_only=True)

    class Meta:
        model = OTPRequest
        fields = ['id', 'otp', 'request_time']

