from django.http import JsonResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import NewsletterEmail

class NewsletterSignupView(View):
    def post(self, request):
        email = request.POST.get('email', '').strip()

        if not email:
            return JsonResponse({'success': False, 'message': 'ایمیل خالی است'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'ایمیل نامعتبر است'}, status=400)

        if NewsletterEmail.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'این ایمیل قبلاً ثبت شده است'}, status=400)

        NewsletterEmail.objects.create(email=email)
        return JsonResponse({'success': True, 'message': 'با موفقیت ثبت شد!'})
    