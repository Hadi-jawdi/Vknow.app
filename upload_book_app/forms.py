from django import forms
from .models import Book


class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file']
        widgets = {
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'required': True
            })
        }
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError("فقط فایل‌های PDF مجاز هستند.")
            if pdf_file.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError("حجم فایل نباید بیشتر از 50 مگابایت باشد.")
        return pdf_file
