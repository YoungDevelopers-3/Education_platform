from ckeditor.fields import RichTextField
from django.db import models

# from apps.lessons.models import Lesson
from apps.shared.models import BaseModel
from apps.users.models import User

DAYS = (
    ("dushanba", "dushanba"),
    ("seshanba", "seshanba"),
    ("chorshanba", "payshanba"),
    ("payshanba", "payshanba"),
    ("juma", "juma"),
    ("shanba", "shanba"),
    ("yakshanba", "yakshanba"),
)


class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_teacher')
    photo = models.ImageField(null=True, blank=True, upload_to=f"teachers/{user}/")
    bio = RichTextField()

    def __str__(self):
        return f"{self.user.username}'s profile"


class Lesson(BaseModel):
    title = models.CharField(max_length=221)
    image = models.ImageField(null=True, blank=True, upload_to=f'lessons/{title}/')
    description = RichTextField()
    teachers = models.ManyToManyField(Teacher, related_name='lessons')

    def __str__(self):
        return self.title


class TimeLesson(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='times')
    day = models.CharField(max_length=15, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.day


class Pupil(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_pupil')
    photo = models.ImageField(null=True, blank=True, upload_to=f"pupils/{user}/")
    bio = RichTextField()
    lessons = models.ManyToManyField(Lesson, related_name='pupils')

    def __str__(self):
        return f"{self.user.username}'s profile"


class Marks(BaseModel):
    mark = models.IntegerField()
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, related_name='marks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='marks')
    time_lesson = models.OneToOneField(TimeLesson, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.pupil.user.username} ga {self.teacher.user.username} {self.mark} baho qo'ydi"
