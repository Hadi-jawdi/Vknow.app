from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    SUBJECT_CHOICES = [
        ('Biology', 'Biology'),
        ('Chemistry', 'Chemistry'),
        ('Dari', 'Dari'),
        ('Geology', 'Geology'),
        ('Math', 'Math'),
        ('Physics', 'Physics'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'آسان'),
        ('medium', 'متوسط'),
        ('hard', 'سخت'),
    ]

    question_id = models.IntegerField()
    question = models.TextField()
    options = models.JSONField()
    correct_option = models.IntegerField()
    correct_answer = models.CharField(max_length=500)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"[{self.subject}] {self.question[:50]}"


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    subject = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, blank=True)
    score = models.IntegerField()
    total = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total == 0:
            return 0
        return round((self.score / self.total) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.subject} - {self.score}/{self.total}"