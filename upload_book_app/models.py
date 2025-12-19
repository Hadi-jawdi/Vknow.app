from django.db import models
from django.contrib.auth.models import User
import os


class Book(models.Model):
    title = models.CharField(max_length=255, blank=True)
    pdf_file = models.FileField(upload_to='books/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_books')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    
    def __str__(self):
        return self.title or f"Book {self.id}"
    
    def delete(self, *args, **kwargs):
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
        super().delete(*args, **kwargs)


class Question(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Q{self.id}: {self.question_text[:50]}..."


class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quiz_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} - Score: {self.score}/{self.total_questions}"
    
    def calculate_percentage(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100, 2)
        return 0


class Answer(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['quiz_session', 'question']
    
    def __str__(self):
        return f"{self.quiz_session.user.username} - Q{self.question.id} - {self.selected_answer}"

