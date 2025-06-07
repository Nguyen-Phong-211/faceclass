from django.urls import path
from .views import csrf_cookie, send_otp, verify_otp

urlpatterns = [
    path('send_otp/', send_otp),
    path('verify_otp/', verify_otp),
    path('csrf/cookie/', csrf_cookie),  
]