from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, OTP, ProfileUser
from .serializers import PhoneNumberSerializers, VerifyOTPSerializers, ProfileUserSerializer, CustomUserSerializer, OTPSerializer, OTPRequestSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class SendOtp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializers = PhoneNumberSerializers(data=request.data)
        if serializers.is_valid():
            phone = serializers.validated_data['phone_number']
            user, created = CustomUser.objects.get_or_create(phone_number=phone)
            existing_otp = OTP.objects.filter(user=user, is_verified=False).last()
            if existing_otp and not  existing_otp.is_expired():
                return Response({"detail":"Previous OTP code is still valid."}, status=status.HTTP_400_BAD_REQUEST)
            otp = OTP.objects.create(user=user)
            print(f'sent otp {otp.code} to {phone}')
            return Response({'detail': 'otp send'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializers = VerifyOTPSerializers(data=request.data)
        print(request.data)
        if serializers.is_valid():
            user = serializers.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUserApi(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ListUserApiDetails(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ListOTPApiDetails(ListAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
