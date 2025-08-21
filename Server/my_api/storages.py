import os
from django.core.files.storage import FileSystemStorage

class FixedNameOverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # 동일 파일 제거
        if self.exists(name):
            self.delete(name)
        return name

    def save(self, name, content, max_length=None):
        # 확장자 바뀌어도 base가 image인 파일 삭제
        dir_name, file_name = os.path.split(name)
        base, _ = os.path.splitext(file_name)
        try:
            _, files = self.listdir(dir_name)
            for f in files:
                if os.path.splitext(f)[0] == base:
                    super().delete(os.path.join(dir_name, f))
        except Exception:
            pass
        return super().save(name, content, max_length=max_length)