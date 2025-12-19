from django.contrib import admin
from .models import Book, Question, QuizSession, Answer


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'question_text', 'correct_answer']
    list_filter = ['book', 'created_at']
    search_fields = ['question_text']


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'score', 'total_questions', 'started_at', 'completed_at']
    list_filter = ['started_at', 'completed_at']
    search_fields = ['user__username', 'book__title']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_session', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
