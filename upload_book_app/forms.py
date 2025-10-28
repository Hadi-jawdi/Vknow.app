from django import forms

class BookUploadForm(forms.Form):
    file = forms.FileField(label="آپلود کتاب", required=True)
