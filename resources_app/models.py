
# from django.db import models
# from django.contrib.auth.models import User

# class ShareResource(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
#     title = models.CharField(max_length=255, verbose_name="عنوان منبع")
#     description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
#     link = models.URLField(blank=True, null=True, verbose_name="لینک (اختیاری)")
#     file = models.FileField(upload_to="shared_resources/", blank=True, null=True, verbose_name="فایل (اختیاری)")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

#     def __str__(self):
        # return self.title

from django.db import models
from django.contrib.auth.models import User
import os

FILE_ICONS = {
    ".pdf": "fa-file-pdf text-danger",
    ".doc": "fa-file-word text-primary",
    ".docx": "fa-file-word text-primary",
    ".ppt": "fa-file-powerpoint text-warning",
    ".pptx": "fa-file-powerpoint text-warning",
    ".jpg": "fa-file-image text-info",
    ".png": "fa-file-image text-info",
    ".mp4": "fa-file-video text-success",
    ".zip": "fa-file-archive text-secondary",
    ".rar": "fa-file-archive text-secondary",
}


class ShareResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=255, verbose_name="عنوان منبع")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    link = models.URLField(blank=True, null=True, verbose_name="لینک (اختیاری)")
    file = models.FileField(upload_to="shared_resources/", blank=True, null=True, verbose_name="فایل (اختیاری)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    def get_file_icon(self):
        """Automatically detect file type and return a FontAwesome icon class."""
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            return FILE_ICONS.get(ext, "fa-file text-gray-400")
        return "fa-link text-blue-400"


class ResourceComment(models.Model):
    resource = models.ForeignKey(ShareResource, on_delete=models.CASCADE, related_name="comments", verbose_name="منبع")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    content = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"نظر {self.user.username} درباره {self.resource.title}"
