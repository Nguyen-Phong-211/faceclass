from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Account 
from accounts.models import Role 
from .serializers import AccountSerializer
from django.middleware.csrf import get_token
import traceback
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .otp_storage import otp_storage
import random
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET'])
@ensure_csrf_cookie
def csrf_cookie(request):
    return JsonResponse({'message': 'CSRF cookie set'})

@api_view(['POST'])
def send_otp(request):
    data = request.data
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not email:
        return Response({'error': 'Email là bắt buộc'}, status=400)

    if Account.objects.filter(email=email).exists():
        return Response({'error': 'Email này đã được đăng ký'}, status=400)

    if phone_number and Account.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'Số điện thoại này đã được đăng ký'}, status=400)

    otp = f"{random.randint(100000, 999999)}"
    cache.set(email, {'otp': otp, 'data': data}, timeout=300)

    send_mail(
        'EDU FACE ID',  
        f'Mã OTP của bạn là: {otp}',  
        'zephyrnguyen.vn@gmail.com', 
        [email],
        fail_silently=False,
    )

    return Response({'message': 'OTP đã được gửi đến email'})


# Save information of user then auth OTP
@api_view(['POST'])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    reset_token = get_token(request)

    print("Email:", email)
    print("OTP:", otp)
    print("CSRF: ", reset_token)

    if not email or not otp:
        return Response({'error': 'Thiếu email hoặc mã OTP'}, status=400)

    stored = cache.get(email) 

    if not stored:
        return Response({'error': 'Không tìm thấy OTP hoặc OTP đã hết hạn'}, status=400)

    if stored['otp'] != otp:
        return Response({'error': 'Mã OTP không đúng'}, status=400)

    user_data = stored['data']
    user_data['password'] = make_password(user_data['password'])
    user_data['reset_token'] = reset_token

    serializer = AccountSerializer(data=user_data)
    if serializer.is_valid():
        account = serializer.save()

        refresh = RefreshToken.for_user(account)
        access_token = str(refresh.access_token)

        print("Access Token: ", access_token)

        cache.delete(email)

        return Response({
            "message": "Đăng ký thành công",
            "user": {
                'account_id': account.account_id,
                'email': account.email,
                'phone_number': account.phone_number,
                'role_id': getattr(account.role, 'role_id', None),
                'reset_token': account.reset_token,
                'user_type': account.user_type,
            },
            "refresh_token": str(refresh),
            "access_token": access_token
        }, status=201)
    else:
        return Response({'error': serializer.errors}, status=400)