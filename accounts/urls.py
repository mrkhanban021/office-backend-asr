from django.urls import path
from .views import (SendOtp, VerifyOTPView, ListUserApi, ListUserApiDetails, ListOTPApiDetails, ProfileDetail)

app_name= "accounts"

urlpatterns =[
    path('sendotp/', SendOtp.as_view(), name='sendotp'),
    path('verifyotp/', VerifyOTPView.as_view(),),
    path('list_user/', ListUserApi.as_view()),
    path('list_user/<int:pk>', ListUserApiDetails.as_view()),
    path('list_otp/', ListOTPApiDetails.as_view()),
    path('profileuser/', ProfileDetail.as_view()),

]
