mport os
from django.db import models
from .storages import FixedNameOverwriteStorage



def fixed_name_upload_to(_, fn):
    ext = os.path.splitext(fn)[1].lower() or '.jpg'
    return f'uploads/image{ext}'

class Page(models.Model):
    
    image = models.ImageField(
        upload_to=fixed_name_upload_to,
        storage=FixedNameOverwriteStorage(),
        blank=False,
        null=False,
    )
