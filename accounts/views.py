from rest_framework.decorators import api_view, permission_classes
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
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import Account
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .serializers import LoginSerializer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import string
from datetime import datetime
from students.models import Student

@api_view(['GET'])
@ensure_csrf_cookie
def csrf_cookie(request):
    return JsonResponse({'message': 'CSRF cookie set'})

@api_view(['POST'])
def send_otp(request):
    data = request.data
    email = data.get("email", "").strip().lower()
    phone_number = data.get('phone_number')

    if not email:
        return Response({'error': 'Email là bắt buộc'}, status=400)

    if Account.objects.filter(email=email).exists():
        return Response({'error': 'Email này đã được đăng ký'}, status=400)

    if phone_number and Account.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'Số điện thoại này đã được đăng ký'}, status=400)

    otp = f"{random.randint(100000, 999999)}"
    cache.set(email, {'otp': otp, 'data': data}, timeout=300)

    subject = 'Mã OTP từ FACE CLASS'
    from_email = 'zephyrnguyen.vn@gmail.com'
    to = [email]

    html_content = render_to_string('account/otp_email.html', {'otp': otp})
    text_content = f'Mã OTP của bạn là: {otp}'

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response({'message': 'OTP đã được gửi đến email'})


# Save information of user then auth OTP
@api_view(['POST'])
def verify_otp(request):
    email = request.data.get("email", "").strip().lower()
    otp = request.data.get("otp")
    reset_token = get_token(request)

    if not email or not otp:
        return Response({'error': 'Thiếu email hoặc mã OTP'}, status=400)

    stored = cache.get(email)

    if not stored:
        print("OTP cache không tồn tại cho:", email)
        return Response({'error': 'Không tìm thấy OTP hoặc OTP đã hết hạn'}, status=400)

    if stored['otp'] != otp:
        return Response({'error': 'Mã OTP không đúng'}, status=400)

    user_data = stored['data']
    # user_data['password'] = make_password(user_data['password'])
    user_data['reset_token'] = reset_token

    serializer = AccountSerializer(data=user_data)
    if serializer.is_valid():
        account = serializer.save()

        refresh = RefreshToken.for_user(account)
        access_token = str(refresh.access_token)

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

@csrf_exempt
@api_view(['POST'])
def update_avatar(request, account_id):
    if request.method == 'POST':
        if 'avatar' not in request.FILES:
            return JsonResponse({'error': 'Không có file avatar được gửi lên'}, status=400)

        avatar_file = request.FILES['avatar']

        avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)

        # Create image's name file
        random_digits = ''.join(random.choices(string.digits, k=10))
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ext = os.path.splitext(avatar_file.name)[1]
        filename = f"avatar_{random_digits}_{timestamp}{ext}"

        filepath = os.path.join(avatar_dir, filename)

        with open(filepath, 'wb+') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)

        avatar_url = 'avatars/' + filename

        # Save image in database
        try:
            account = Account.objects.get(account_id=account_id)
            account.avatar_url = avatar_url 
            account.save()
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Không tìm thấy tài khoản'}, status=404)

        return JsonResponse({
            'message': 'Upload avatar thành công',
            'avatar_url': settings.MEDIA_URL + avatar_url,
        })

    return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            student_data = {}
            if hasattr(user, 'role') and user.role.role_name == "student":
                try:
                    student = user.student
                    student_data = {
                        "fullname": student.fullname,
                        "student_code": student.student_code,
                        "student_id": student.student_id
                    }
                except Exception as e:
                    student_data = {}

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "account_id": user.account_id,
                    "role": user.role.role_name if user.role else None,
                    **student_data,
                }
            })

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)