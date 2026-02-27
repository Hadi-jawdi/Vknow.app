import random
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Question, TestResult


@login_required
def kankor_home(request):
    subjects = Question.objects.values_list('subject', flat=True).distinct()
    recent_results = TestResult.objects.filter(user=request.user).order_by('-taken_at')[:5]
    return render(request, 'kankoor_app/kankoor_home.html', {
        'subjects': subjects,
        'recent_results': recent_results,
    })


@login_required
def start_test(request):
    subject = request.GET.get('subject', '')
    difficulty = request.GET.get('difficulty', '')
    count = int(request.GET.get('count', 20))

    questions = Question.objects.all()
    if subject:
        questions = questions.filter(subject=subject)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    questions = list(questions)
    if len(questions) < count:
        count = len(questions)

    selected = random.sample(questions, count)

    questions_data = []
    for q in selected:
        questions_data.append({
            'id': q.id,
            'question': q.question,
            'options': q.options,
            'subject': q.subject,
            'difficulty': q.difficulty,
        })

    return render(request, 'kankoor_app/test.html', {
        'questions': questions_data,
        'questions_json': json.dumps(questions_data, ensure_ascii=False),
        'subject': subject or 'همه مضامین',
        'difficulty': difficulty,
        'count': count,
        'timer_minutes': count * 2,
    })


@login_required
@require_POST
def submit_test(request):
    data = json.loads(request.body)
    answers = data.get('answers', {})
    subject = data.get('subject', '')
    difficulty = data.get('difficulty', '')

    score = 0
    results = []

    for q_id, selected in answers.items():
        try:
            question = Question.objects.get(id=int(q_id))
            is_correct = int(selected) == question.correct_option
            if is_correct:
                score += 1
            results.append({
                'question': question.question,
                'options': question.options,
                'selected': int(selected),
                'correct_option': question.correct_option,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
            })
        except Question.DoesNotExist:
            pass

    total = len(results)

    TestResult.objects.create(
        user=request.user,
        subject=subject,
        difficulty=difficulty,
        score=score,
        total=total,
    )

    return JsonResponse({
        'score': score,
        'total': total,
        'percentage': round((score / total) * 100) if total else 0,
        'results': results,
    })