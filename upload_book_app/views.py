from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Book, Question, QuizSession, Answer
from .forms import BookUploadForm
from .utils import extract_text_from_pdf, generate_questions_from_text
import os


@login_required
def upload_book(request):
    """
    Handle book upload and generate questions
    """
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            
            # Extract text from PDF
            try:
                pdf_file = request.FILES['pdf_file']
                book.pdf_file = pdf_file
                extracted_text = extract_text_from_pdf(pdf_file)
                book.extracted_text = extracted_text
                book.title = pdf_file.name.replace('.pdf', '')
                book.save()
                
                # Generate questions
                questions_data = generate_questions_from_text(extracted_text, num_questions=10)
                
                # Save questions to database
                for q_data in questions_data:
                    Question.objects.create(
                        book=book,
                        question_text=q_data['question_text'],
                        option_a=q_data['option_a'],
                        option_b=q_data['option_b'],
                        option_c=q_data['option_c'],
                        option_d=q_data['option_d'],
                        correct_answer=q_data['correct_answer']
                    )
                
                messages.success(request, f'کتاب با موفقیت آپلود شد و {len(questions_data)} سوال ایجاد شد.')
                return redirect('upload_book_app:start_quiz', book_id=book.id)
            except Exception as e:
                messages.error(request, f'خطا در پردازش فایل: {str(e)}')
                if book.pk:
                    book.delete()
    else:
        form = BookUploadForm()
    
    return render(request, 'upload_book_app/pages/upload.html', {'form': form})


@login_required
def start_quiz(request, book_id):
    """
    Start a new quiz session for a book
    """
    book = get_object_or_404(Book, id=book_id)
    questions = Question.objects.filter(book=book)
    
    if not questions.exists():
        messages.error(request, 'هیچ سوالی برای این کتاب یافت نشد.')
        return redirect('upload_book_app:upload_book')
    
    # Create a new quiz session
    quiz_session = QuizSession.objects.create(
        user=request.user,
        book=book,
        total_questions=questions.count()
    )
    
    return redirect('upload_book_app:take_quiz', session_id=quiz_session.id)


@login_required
def take_quiz(request, session_id):
    """
    Display quiz questions
    """
    quiz_session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    if quiz_session.completed_at:
        messages.info(request, 'این آزمون قبلاً تکمیل شده است.')
        return redirect('upload_book_app:quiz_results', session_id=quiz_session.id)
    
    questions = Question.objects.filter(book=quiz_session.book).order_by('id')
    answered_question_ids = Answer.objects.filter(quiz_session=quiz_session).values_list('question_id', flat=True)
    
    # Get current question (first unanswered)
    current_question = None
    for question in questions:
        if question.id not in answered_question_ids:
            current_question = question
            break
    
    if not current_question:
        # All questions answered, complete the quiz
        return redirect('upload_book_app:submit_quiz', session_id=quiz_session.id)
    
    # Get question number
    question_number = len(answered_question_ids) + 1
    
    # Calculate progress percentage
    progress_percent = int((question_number / quiz_session.total_questions) * 100) if quiz_session.total_questions > 0 else 0
    
    context = {
        'quiz_session': quiz_session,
        'question': current_question,
        'question_number': question_number,
        'total_questions': quiz_session.total_questions,
        'progress_percent': progress_percent,
    }
    
    return render(request, 'upload_book_app/pages/quiz.html', context)


@login_required
@require_POST
def submit_answer(request, session_id):
    """
    Submit an answer for a question
    """
    quiz_session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    if quiz_session.completed_at:
        return JsonResponse({'error': 'Quiz already completed'}, status=400)
    
    question_id = request.POST.get('question_id')
    selected_answer = request.POST.get('answer')
    
    if not question_id or not selected_answer:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    question = get_object_or_404(Question, id=question_id, book=quiz_session.book)
    
    # Check if answer already exists
    answer, created = Answer.objects.get_or_create(
        quiz_session=quiz_session,
        question=question,
        defaults={'selected_answer': selected_answer}
    )
    
    if not created:
        answer.selected_answer = selected_answer
        answer.save()
    
    # Check if correct
    answer.is_correct = (selected_answer.upper() == question.correct_answer)
    answer.save()
    
    return JsonResponse({
        'success': True,
        'is_correct': answer.is_correct,
        'correct_answer': question.correct_answer
    })


@login_required
def submit_quiz(request, session_id):
    """
    Complete the quiz and calculate results
    """
    quiz_session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    if quiz_session.completed_at:
        return redirect('upload_book_app:quiz_results', session_id=quiz_session.id)
    
    # Calculate score
    correct_answers = Answer.objects.filter(quiz_session=quiz_session, is_correct=True).count()
    quiz_session.score = correct_answers
    quiz_session.completed_at = timezone.now()
    quiz_session.save()
    
    return redirect('upload_book_app:quiz_results', session_id=quiz_session.id)


@login_required
def quiz_results(request, session_id):
    """
    Display quiz results
    """
    quiz_session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    answers = Answer.objects.filter(quiz_session=quiz_session).select_related('question')
    
    context = {
        'quiz_session': quiz_session,
        'answers': answers,
        'percentage': quiz_session.calculate_percentage(),
    }
    
    return render(request, 'upload_book_app/pages/results.html', context)


@login_required
def my_books(request):
    """
    Display user's uploaded books
    """
    books = Book.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'upload_book_app/pages/my_books.html', {'books': books})
