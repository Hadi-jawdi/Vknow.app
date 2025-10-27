
from django.db import models
from django.contrib.auth.models import User

class DiscussionPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    content = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    def __str__(self):
        return self.title

class DiscussionReply(models.Model):
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE, related_name="replies", verbose_name="پست اصلی")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    content = models.TextField(verbose_name="متن پاسخ")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="child_replies", verbose_name="پاسخ به")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post.title}"
