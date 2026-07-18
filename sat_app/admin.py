from django.contrib import admin

from .models import SATAttemptAnswer, SATQuestion, SATTestAttempt


@admin.register(SATQuestion)
class SATQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "section", "domain", "difficulty", "short_question", "source")
    list_filter = ("section", "domain", "difficulty", "source")
    search_fields = ("question_text", "paragraph", "external_id")

    def short_question(self, obj):
        return obj.question_text[:80]

    short_question.short_description = "Question"


class SATAttemptAnswerInline(admin.TabularInline):
    model = SATAttemptAnswer
    extra = 0
    readonly_fields = ("question", "order", "selected_answer", "is_correct", "answered_at")
    can_delete = False


@admin.register(SATTestAttempt)
class SATTestAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "section", "status", "score", "total_questions", "started_at")
    list_filter = ("section", "status")
    search_fields = ("user__username", "user__email")
    inlines = [SATAttemptAnswerInline]
