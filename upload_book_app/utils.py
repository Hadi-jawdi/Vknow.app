import re
import random

# PDF reading library - supports both pypdf (modern) and PyPDF2 (legacy)
try:
    from pypdf import PdfReader  # type: ignore
    PDF_LIBRARY_AVAILABLE = True
except ImportError:
    try:
        from PyPDF2 import PdfReader  # type: ignore
        PDF_LIBRARY_AVAILABLE = True
    except ImportError:
        PdfReader = None
        PDF_LIBRARY_AVAILABLE = False


def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF file
    """
    if not PDF_LIBRARY_AVAILABLE or PdfReader is None:
        raise ImportError(
            "کتابخانه PDF یافت نشد. لطفاً یکی از کتابخانه‌های زیر را نصب کنید:\n"
            "pip install pypdf\n"
            "یا\n"
            "pip install PyPDF2"
        )
    
    try:
        # Reset file pointer to beginning in case it was read before
        if hasattr(pdf_file, 'seek'):
            pdf_file.seek(0)
        
        pdf_reader = PdfReader(pdf_file)
        
        if len(pdf_reader.pages) == 0:
            raise Exception("فایل PDF خالی است یا قابل خواندن نیست")
        
        text = ""
        # Extract text from first 50 pages to avoid processing very long books
        max_pages = min(50, len(pdf_reader.pages))
        for page_num in range(max_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            raise Exception("نتوانستیم متن را از فایل PDF استخراج کنیم. ممکن است فایل اسکن شده باشد یا متن قابل استخراج نداشته باشد")
        
        # Clean up text
        text = re.sub(r'\s+', ' ', text)
        return text[:50000]  # Limit to 50000 characters for question generation
    except ImportError as e:
        raise ImportError(f"خطا در وارد کردن کتابخانه PDF: {str(e)}")
    except Exception as e:
        raise Exception(f"خطا در خواندن فایل PDF: {str(e)}")


def generate_questions_from_text(text, num_questions=5):
    """
    Generate multiple choice questions from text
    """
    questions = []
    
    # Split text into sentences
    sentences = re.split(r'[.!?]\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if len(sentences) < num_questions:
        num_questions = len(sentences)
    
    # Simple question generation: create questions from key sentences
    selected_indices = random.sample(range(len(sentences)), min(num_questions, len(sentences)))
    
    for idx, i in enumerate(selected_indices):
        sentence = sentences[i]
        # Create a simple question based on the sentence
        question_text = f"متن زیر را بخوانید و بهترین گزینه را انتخاب کنید:\n\n{sentence[:300]}"
        
        # Create simple options with variations
        # In a real implementation, AI would generate meaningful distractors
        options = {
            'A': 'این متن در مورد موضوع اصلی صحبت می‌کند',
            'B': 'این متن یک مثال است',
            'C': 'این متن یک توضیح اضافی است',
            'D': 'این متن مربوط به موضوع دیگری است'
        }
        
        # Rotate correct answer for variety
        correct_answer = ['A', 'B', 'C', 'D'][idx % 4]
        
        questions.append({
            'question_text': question_text,
            'option_a': options['A'],
            'option_b': options['B'],
            'option_c': options['C'],
            'option_d': options['D'],
            'correct_answer': correct_answer
        })
    
    return questions

