import uuid
from random import randint

from django.template.context_processors import static
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from apps.shared.utils import check_email, send_email
from apps.users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, email):
        if check_email(email):
            print(2)
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    {
                        'description': "Bunday email allaqachon ishlatilgan, boshqa email kiritib ko'ring",
                        'status': status.HTTP_400_BAD_REQUEST
                    }
                )
            user = self.create_user(email)
            code = user.create_verification_code()
            send_email(email, code)

            return email
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
