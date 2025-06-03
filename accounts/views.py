from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, OTP, ProfileUser
from .serializers import PhoneNumberSerializers, VerifyOTPSerializers, CustomUserSerializer, OTPSerializer, ProfileUserSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from worklog.signals import user_logged_in_signal
from .webonesms.config import send_otp_message
from djangoProject.core.permissions import CustomerAccessPermission


class SendOtp(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=PhoneNumberSerializers,
        responses={200: None},
        description="به شماره موبایل کاربر (اگر ثبتنام نکرده باشد ثبتنام میشود) در غیر اینصورت otp ارسال میشود",
        examples=[
            OpenApiExample(
                "مثال موفق",
                value={"phone_number": "09123456789"},
                request_only=True

            )
        ]
    )
    def post(self, request):
        serializers = PhoneNumberSerializers(data=request.data)
        if serializers.is_valid():
            phone = serializers.validated_data['phone_number']
            user, created = CustomUser.objects.get_or_create(phone_number=phone)
            existing_otp = OTP.objects.filter(user=user, is_verified=False).last()
            if existing_otp and not existing_otp.is_expired():
                return Response({"detail": "Previous OTP code is still valid."}, status=status.HTTP_400_BAD_REQUEST)
            otp = OTP.objects.create(user=user)
            print(f'{phone} - {otp.code}')
            # # sent = send_otp_message(phone, otp.code)
            # if sent.get("succeeded") == False:
            #     return Response({"detail": "call system administrator"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'otp send'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=VerifyOTPSerializers,
        responses={
            200: OpenApiResponse(
                description="درخواست موفقیت آمیز است، توکن‌ها ارسال می‌شوند",
                examples=[
                    OpenApiExample(
                        "موفقیت",
                        value={
                            "refresh": "your_refresh_token_here",
                            "access": "your_access_token_here"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="درخواست نامعتبر است (به عنوان مثال کد OTP اشتباه است)"
            )
        },
        description="وقتی کد یک بار مصرف ارسال بشه واردش کنی اینجا بهت یک توکن برای احراز هویت میده",
        examples=[
            OpenApiExample(
                "نمونه درخواست",
                value={
                    "phone_number": "09123456789",  # شماره موبایل کاربر
                    "otp": "123456"  # کد OTP وارد شده توسط کاربر
                },
                request_only=True
            )
        ]
    )
    def post(self, request):
        serializers = VerifyOTPSerializers(data=request.data)
        if serializers.is_valid():
            user = serializers.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            user_logged_in_signal.send(sender=user.__class__, user=user, request=request)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id
                }
            }, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUserApi(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [CustomerAccessPermission]



class ListUserApiDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)


class ListOTPApiDetails(ListAPIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    permission_classes = (IsAdminUser,)


class ProfileDetail(RetrieveUpdateAPIView):
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return ProfileUser.objects.get(user=self.request.user)


