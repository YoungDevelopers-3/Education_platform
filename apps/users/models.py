from datetime import datetime, timedelta
from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.shared.models import BaseModel

ROLE = (
    ('begona', 'begona'),
    ('admin', 'admin'),
    ('teacher', 'teacher'),
    ('pupil', 'pupil'),
)

STATUS = (
    ('new', 'new'),
    ('code', 'code'),
    ('done', 'done'),
)


class Role(BaseModel):
    name = models.CharField(max_length=10, choices=ROLE, default='begona', unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=17, unique=True, null=True, blank=True)
    role = models.ManyToManyField(Role)
    status = models.CharField(choices=STATUS, default='new')

    def create_verify_code(self):
        code = "".join([str(randint(1, 10) % 10) for i in range(4)])
        UserVerification.objects.create(
            user_id=self.id,
            code=code,
            time_limit=datetime.now() + timedelta(minutes=5)
        )
        return code

    def __str__(self):
        return self.username


class UserVerification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verifications')
    code = models.CharField(max_length=4)
    time_limit = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s verification ({self.id})"
