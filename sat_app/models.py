import uuid

from django.conf import settings
from django.db import models


class SATQuestion(models.Model):
    """
    A single SAT practice question, imported from an external source
    (OpenSAT JSON dataset) and stored locally so the site never depends
    on a third-party API at request time.
    """

    class Section(models.TextChoices):
        READING_WRITING = "RW", "Reading and Writing"
        MATH = "MATH", "Math"

    class Difficulty(models.TextChoices):
        EASY = "Easy", "Easy"
        MEDIUM = "Medium", "Medium"
        HARD = "Hard", "Hard"

    # Stable identifier so re-running the import doesn't create duplicates.
    external_id = models.CharField(max_length=64, unique=True, db_index=True)

    section = models.CharField(max_length=8, choices=Section.choices, default=Section.READING_WRITING)

    # e.g. "Information and Ideas", "Standard English Conventions",
    # or for math: "Algebra", "Geometry and Trigonometry", etc.
    domain = models.CharField(max_length=128, blank=True)

    difficulty = models.CharField(max_length=8, choices=Difficulty.choices, default=Difficulty.MEDIUM)

    # The passage/stimulus text shown above the question (can be empty).
    paragraph = models.TextField(blank=True)

    question_text = models.TextField()

    choice_a = models.TextField()
    choice_b = models.TextField()
    choice_c = models.TextField()
    choice_d = models.TextField()

    correct_answer = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])

    explanation = models.TextField(blank=True)

    # Optional inline SVG for math questions with a figure/graph.
    # Rendered with your existing KaTeX pipeline for LaTeX inside question_text.
    svg_content = models.TextField(blank=True)

    source = models.CharField(max_length=64, default="opensat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["section", "domain"]),
            models.Index(fields=["section", "difficulty"]),
        ]

    def __str__(self):
        return f"[{self.section}] {self.question_text[:60]}"

    @property
    def choices(self):
        return {
            "A": self.choice_a,
            "B": self.choice_b,
            "C": self.choice_c,
            "D": self.choice_d,
        }


class SATTestAttempt(models.Model):
    """One user's attempt at a practice set (a 'test')."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sat_attempts")

    section = models.CharField(max_length=8, choices=SATQuestion.Section.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IN_PROGRESS)

    questions = models.ManyToManyField(SATQuestion, through="SATAttemptAnswer")

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Denormalized for fast history/leaderboard queries.
    score = models.PositiveIntegerField(null=True, blank=True)
    total_questions = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user} — {self.get_section_display()} — {self.started_at:%Y-%m-%d}"

    @property
    def percent_correct(self):
        if not self.total_questions:
            return 0
        return round((self.score or 0) / self.total_questions * 100)


class SATAttemptAnswer(models.Model):
    """The user's answer (or lack of one) to a single question within an attempt."""

    attempt = models.ForeignKey(SATTestAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SATQuestion, on_delete=models.CASCADE)

    order = models.PositiveSmallIntegerField()
    selected_answer = models.CharField(max_length=1, blank=True, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")])
    is_correct = models.BooleanField(null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("attempt", "question")

    def save(self, *args, **kwargs):
        if self.selected_answer:
            self.is_correct = self.selected_answer == self.question.correct_answer
        super().save(*args, **kwargs)
