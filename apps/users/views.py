from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenRefreshView

from apps.shared.utils import send_email
from apps.users.models import User, UserVerification
from apps.users.serializers import SignUpSerializer, UserFillingDataSerializer, LoginSerializer, LoginRefreshSerializer, \
    LogOutSerializer


class SignUpApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User.objects.all(), email=email)
        refresh_token = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
        data = serializer.data
        data['tokens'] = tokens
        return Response({
            'data': data,
            'description': "Emailingizga tasdiqlash kodi yuborildi",
            'status': status.HTTP_201_CREATED
        })


class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = request.data.get('code')
        user = request.user
        verifies = UserVerification.objects.filter(
            Q(user=user) & Q(time_limit__gt=datetime.now()) & Q(is_confirmed=False) & Q(code=code))
        if verifies.exists():
            verify = verifies.first()
            verify.is_confirmed = True
            user.status = 'code'
            user.save()
            tokens = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user=user)
            return Response(
                {
                    'description': "Kod muvaffaqiyatli tasdiqlandi",
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'status': status.HTTP_200_OK,
                }
            )
        return Response(
            {
                'description': "Siz noto'g'ri kod kiritdingiz",
                'status': status.HTTP_400_BAD_REQUEST
            }
        )


class VerifyAgainApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        verifications = user.verifications.filter(is_confirmed=False, time_limit__gt=datetime.now())
        if verifications.exists():
            raise ValidationError(
                {
                    'detail': "Sizda yaroqli kod mavjud, iltimos biroz kuting!",
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
        else:
            code = user.create_verify_code()
            send_email(user.email, code)
            return Response({
                'detail': 'Emailingizga yangi tasdiqlash kodi yuborildi',
                'status': status.HTTP_200_OK
            })


class UserFillingDataApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        role = request.data.get('role_name')
        user = request.user
        if user.status == "new":
            raise PermissionDenied('Sizda ruxsat yo\'q')
        data = request.data
        validate_password(password)
        if password != confirm_password:
            raise ValidationError(
                {
                    'description': 'Password va Confirm_password bir-biriga teng emas',
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

        serializer = UserFillingDataSerializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        print('serializer_data', serializer.validated_data)
        serializer.save()
        user.set_password(password)
        user.status = 'done'
        user.save()
        print(user.role.all())
        return Response(
            {
                'data': serializer.data,
                'description': 'Sizning ma\'lumotlaringiz muvaffaqiyatli to\'ldirildi',
                'status': status.HTTP_200_OK
            }
        )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'data': serializer.validated_data,
                'status': status.HTTP_200_OK
            }
        )


class LoginRefreshApiView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogOutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        serializer = LogOutSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "detail": "You are successfully logged out"
            }
            return Response(data, status=205)
        except:
            return Response(status=400)
