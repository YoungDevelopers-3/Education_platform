from django.urls import path

from apps.profiles.views import TeacherCreateDeleteApiView, PupilCreateDeleteApiView, ChangeProfileApiView

app_name = 'profiles'

urlpatterns = [
    path('create-teacher/', TeacherCreateDeleteApiView.as_view()),
    path('create-pupil/', PupilCreateDeleteApiView.as_view()),
    path('change-profile/', ChangeProfileApiView.as_view())
]
