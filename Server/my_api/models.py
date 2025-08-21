mport os
from django.db import models
from .storages import FixedNameOverwriteStorage

def upload_to(instance, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower() or '.jpg'
    # 항상 uploads/image.<확장자> 로 저장
    return f'uploads/image{ext}'

class Page(models.Model):
    #필드명 항상 IMAGE로 저장
    image = models.ImageField(
        upload_to=upload_to,
        storage=FileStorage(),
        blank=False,
        null=False,
    )
