from fileinput import filename

from django.core.files.storage import FileSystemStorage
from django.db import models
import os
from django.conf import settings

def date_upload_to(instance, filename):
  extension = os.path.splitext(filename)[-1].lower()
  if (os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'uploads', 'image'+extension))):
    os.remove(os.path.join(settings.MEDIA_ROOT, 'uploads', 'image'+extension))
  path = 'uploads'
  imageName = "image"
  # 확장자 추출
  # 결합 후 return
  return '/'.join([
    path,
    imageName + extension,
  ])


class Page(models.Model):
  image = models.ImageField(upload_to=date_upload_to)