import uuid
import phonenumbers
from random import randint

from django.contrib.auth.password_validation import validate_password
from django.template.context_processors import static
from phonenumbers import NumberParseException
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from apps.shared.utils import check_email, send_email
from apps.users.models import User


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
            print('number_parse_exaption')
            raise ValidationError(
                {
                    'description': "Ushbu telefon raqami to'g'ri emas",
                    'maslahat': "+9980000000 ko'rinishida telefon raqami kiriting !",
                    'status': status.HTTP_400_BAD_REQUEST
                }
            )
