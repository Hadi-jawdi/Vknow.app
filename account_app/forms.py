
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری خود را وارد کنید',
                'autofocus': True,
            }
        ),
    )

    email = forms.EmailField(
        label="ایمیل",
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com',
            }
        ),
    )

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'حداقل ۸ کاراکتر',
            }
        ),
        help_text="رمز عبور باید حداقل ۸ کاراکتر باشد.",
    )

    password2 = forms.CharField(
        label="تأیید رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'رمز عبور را دوباره وارد کنید',
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, label='نام')
    last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
        labels = {
            'profile_picture': 'تصویر پروفایل',
            'bio': 'درباره من',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.save()
        if commit:
            profile.save()
        return profile