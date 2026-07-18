import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import StartTestForm
from .models import SATAttemptAnswer, SATQuestion, SATTestAttempt


@login_required
def start_test(request):
    if request.method == "POST":
        form = StartTestForm(request.POST)
        if form.is_valid():
            section = form.cleaned_data["section"]
            num_questions = int(form.cleaned_data["num_questions"])
            domain = form.cleaned_data["domain"]

            pool = SATQuestion.objects.filter(section=section)
            if domain:
                pool = pool.filter(domain=domain)

            pool_ids = list(pool.values_list("id", flat=True))
            if len(pool_ids) < 1:
                form.add_error(None, "No questions are available for that selection yet.")
            else:
                sample_size = min(num_questions, len(pool_ids))
                chosen_ids = random.sample(pool_ids, sample_size)

                attempt = SATTestAttempt.objects.create(
                    user=request.user,
                    section=section,
                    total_questions=sample_size,
                )
                SATAttemptAnswer.objects.bulk_create([
                    SATAttemptAnswer(attempt=attempt, question_id=qid, order=i)
                    for i, qid in enumerate(chosen_ids, start=1)
                ])
                return redirect("sat:take_test", attempt_id=attempt.id)
    else:
        form = StartTestForm()

    return render(request, "sat_app/start_test.html", {"form": form})


@login_required
def take_test(request, attempt_id):
    attempt = get_object_or_404(
        SATTestAttempt, id=attempt_id, user=request.user, status=SATTestAttempt.Status.IN_PROGRESS
    )
    answers = (
        attempt.answers
        .select_related("question")
        .order_by("order")
    )
    return render(request, "sat_app/take_test.html", {"attempt": attempt, "answers": answers})


@login_required
@require_POST
def submit_test(request, attempt_id):
    attempt = get_object_or_404(
        SATTestAttempt, id=attempt_id, user=request.user, status=SATTestAttempt.Status.IN_PROGRESS
    )

    score = 0
    for ans in attempt.answers.select_related("question"):
        selected = request.POST.get(f"q_{ans.question_id}", "")
        if selected in ("A", "B", "C", "D"):
            ans.selected_answer = selected
            ans.answered_at = timezone.now()
            ans.save()  # is_correct computed in model.save()
            if ans.is_correct:
                score += 1

    attempt.score = score
    attempt.status = SATTestAttempt.Status.COMPLETED
    attempt.completed_at = timezone.now()
    attempt.save()

    return redirect("sat_app:test_results", attempt_id=attempt.id)


@login_required
def test_results(request, attempt_id):
    attempt = get_object_or_404(SATTestAttempt, id=attempt_id, user=request.user)
    answers = (
        attempt.answers
        .select_related("question")
        .order_by("order")
    )
    return render(request, "sat_app/test_results.html", {"attempt": attempt, "answers": answers})


@login_required
def test_history(request):
    attempts = (
        SATTestAttempt.objects.filter(user=request.user, status=SATTestAttempt.Status.COMPLETED)
        .order_by("-started_at")
    )
    return render(request, "sat_app/test_history.html", {"attempts": attempts})
