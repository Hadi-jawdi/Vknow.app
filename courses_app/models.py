from django.db import models

# Create your models here.

from django.db import models

class Courses(models.Model):
    course_name = models.CharField(max_length=255, verbose_name="نام دوره")
    course_banner = models.ImageField(upload_to='course_banners/', verbose_name="بنر دوره")
    course_title = models.CharField(max_length=255, verbose_name="عنوان دوره")
    course_description = models.TextField(verbose_name="توضیحات دوره")

    def __str__(self):
        return self.course_name


class CourseLesson(models.Model):
    lesson_name = models.CharField(max_length=255, verbose_name="نام درس")
    # lesson = pas
    lesson_banner = models.ImageField(upload_to='lesson_banners/', verbose_name="بنر درس")
    lesson_title = models.CharField(max_length=255, verbose_name="عنوان درس")
    lesson_description = models.TextField(verbose_name="توضیحات درس")
    
    # Link lesson to a course
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lessons', verbose_name="دوره مربوطه")

    def __str__(self):
        return self.lesson_name