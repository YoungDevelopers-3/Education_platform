from django.db import models
from ckeditor.fields import RichTextField

from apps.shared.models import BaseModel
from apps.users.models import User


class Images(BaseModel):
    image = models.ImageField(upload_to='news', null=True, blank=True)


class News(BaseModel):
    title = models.CharField(max_length=200)
    description = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    images = models.ForeignKey(Images, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
