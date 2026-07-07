from django.db import models

class Scholarship(models.Model):
    
    LEVEL_CHOICES = [
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PHD'),
        ('all','All'),
    ]

    FIELD_CHOICES = [
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine'),
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('business', 'Business'),
        ('law', 'Law'),
        ('other', 'Other'),
        ('all', "All")
    ]

    title        = models.CharField(max_length=255)           # نام بورسیه
    country      = models.CharField(max_length=100)           # کشور
    university   = models.CharField(max_length=255, blank=True)  # دانشگاه
    level        = models.CharField(max_length=20, choices=LEVEL_CHOICES)  # مقطع
    field        = models.CharField(max_length=50, choices=FIELD_CHOICES)  # رشته
    description  = models.TextField(blank=True)               # توضیحات
    link         = models.URLField(blank=True)                 # لینک
    end_date     = models.CharField(null=True, blank=True)    # مهلت درخواست
    is_active    = models.BooleanField(default=True)          # فعال/غیرفعال
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['end_date']
        verbose_name = 'بورسیه'
        verbose_name_plural = 'بورسیه‌ها'

    def __str__(self):
        return f"{self.title} — {self.country}"