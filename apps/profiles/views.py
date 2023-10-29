from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import Pupil, Teacher
from apps.profiles.permissions import IsAdminUser
from apps.profiles.serializer import TeacherSerializer, PupilSerializer
from apps.users.models import User


class TeacherCreateDeleteApiView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        user_id = request.data.get('user_id')
        if User.objects.filter(id=user_id).exists():
            teacher = User.objects.get(id=user_id)

            roles = [i.id for i in teacher.role.all()]
            if 3 in roles:
                roles.remove(3)
                t = Teacher.objects.get(user_id=user_id)
                t.delete()
            else:
                roles.append(3)
                Teacher.objects.create(user_id=user_id)

            teacher.role.set(roles)
            teacher.save()

            return Response(
                {
                    'description': 'That user\'s role changed successfully',
                },
                status=200
            )


class PupilCreateDeleteApiView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        user_id = request.data.get('user_id')
        if User.objects.filter(id=user_id).exists():
            pupil = User.objects.get(id=user_id)

            roles = [i.id for i in pupil.role.all()]
            if 4 in roles:
                roles.remove(4)
                p = Pupil.objects.get(user_id=user_id)
                p.delete()
            else:
                roles.append(4)
                Pupil.objects.create(user_id=user_id)

            pupil.role.set(roles)
            pupil.save()
            return Response(
                {
                    'description': 'That user\'s role changed successfully',
                },
                status=200
            )


class ChangeProfileApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        user_roles = [i.id for i in user.role.all()]
        if 3 in user_roles or 4 in user_roles:
            if Teacher.objects.filter(user_id=user.id).exists():
                instance = Teacher.objects.get(user_id=user.id)
                print(1)
                serializer = TeacherSerializer(data=request.data, instance=instance)
                print(2)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            if Pupil.objects.filter(user_id=user.id).exists():
                instance = Pupil.objects.get(user_id=user.id)
                serializer = PupilSerializer(data=request.data, instance=instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({
                'description': "Your personal information has changed",
            },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': "you have not got that permission for change information"
                }
            )
