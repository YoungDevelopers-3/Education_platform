import uuid
import phonenumbers
from random import randint

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.template.context_processors import static
from phonenumbers import NumberParseException
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.shared.utils import check_email, send_email, check_username_email_or_phone
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email')
        if check_email(email):
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    {
                        'description': "Bunday email allaqachon ishlatilgan, boshqa email kiritib ko'ring",
                        'status': status.HTTP_400_BAD_REQUEST
                    }
                )
            user = self.create_user(email)
            code = user.create_verify_code()
            send_email(email, code)

            return attrs
        else:
            raise ValidationError(
                {
                    'description': "Bu email bo'la olmaydi",
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )

    def create_user(self, email):
        username = f"username-{uuid.uuid4().__str__().split('-')[-1]}"
        while User.objects.filter(username=username).exists():
            username += str(randint(1000, 9999))
        password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
        user = User.objects.create_user(email=email, username=username)
        user.set_password(password)
        user.save()
        return user


class UserFillingDataSerializer(serializers.ModelSerializer):
    role_name = serializers.StringRelatedField(source='role.name')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'role_name', 'password')
        extra_kwargs = {
            "password": {"required": True}
        }

    def validate_phone(self, phone):
        try:
            x = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(x):
                raise ValidationError(
                    {
                        'description': "Invalid phone number",
                        'status': status.HTTP_400_BAD_REQUEST
                    }
                )
            return phone
        except NumberParseException:
            raise ValidationError(
                {
                    'description': "Ushbu telefon raqami to'g'ri emas",
                    'maslahat': "+9980000000 ko'rinishida telefon raqami kiriting !",
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )


class LoginSerializer(serializers.Serializer):
    username_email_phone = serializers.CharField(max_length=70, required=True)
    password = serializers.CharField(max_length=20, required=True)

    def validate(self, attrs):
        username_email_phone = attrs.pop('username_email_phone')
        password = attrs.pop('password')
        by = check_username_email_or_phone(username_email_phone)
        if by == 'email':
            user = User.objects.filter(email=username_email_phone)
            if user.exists():
                username = user.first().username
            else:
                raise ValidationError(
                    {
                        'detail': "Bunday emailli foydalanuvchi topilmadi",
                        'status': status.HTTP_404_NOT_FOUND
                    }
                )
        elif by == 'phone':
            user = User.objects.filter(phone=username_email_phone)
            if user.exists():
                username = user.first().username
            else:
                raise ValidationError(
                    {
                        'detail': "Bunday telefon raqamli foydalanuvchi topilmadi",
                        'status': status.HTTP_404_NOT_FOUND
                    }
                )
        else:
            user = User.objects.filter(username=username_email_phone)
            if user.exists():
                username = username_email_phone
            else:
                raise ValidationError(
                    {
                        'detail': "Bunday foydalanuvchi topilmadi",
                        'status': status.HTTP_404_NOT_FOUND
                    }
                )
        print('username', username)
        user = authenticate(username=username, password=password)
        if user:
            if user.status != 'done':
                raise PermissionDenied(
                    {
                        'detail': "Sizning ruxsatingiz yo'q, iltimos ma'lumotlaringizni to'ldiring!",
                        'status': status.HTTP_400_BAD_REQUEST,
                    }
                )
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            attrs['tokens'] = tokens
        else:
            raise ValidationError(
                {
                    'detail': "Kiritgan ma'lumotlardan biri noto'g'ri, qayta urunib ko'ring!",
                    'status': status.HTTP_404_NOT_FOUND
                }
            )
        return attrs


class LoginRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attr):
        data = super(LoginRefreshSerializer, self).validate(attr)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance.get('user_id')
        user = get_object_or_404(User.objects.all(), id=user_id)
        update_last_login(None, user)
        print('data', data)
        return data


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
