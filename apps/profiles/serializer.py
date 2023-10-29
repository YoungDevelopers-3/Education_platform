from rest_framework import serializers
from .models import Teacher, Pupil
from ..users.serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'photo', 'bio')


class PupilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'photo', 'bio', 'lessons')
        extra_kwargs = {
            'lessons': {
                'required': False,
            }
        }
