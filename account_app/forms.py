from django import forms
# from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# for registering user with email 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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



# # class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone_number','address']
#         widgets = {
           
#             'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone_Number'}),
#             'address': forms.Textarea(attrs={'class': 'form-control',  'placeholder': 'Your Address'}),
#         }
#     # for validating the form
#     def clean(self):
#         cleaned_data = super().clean()
#         phone_number = cleaned_data.get('phone_number')
#         address = cleaned_data.get('address')

#         if phone_number is None or len(phone_number) < 10:
#                  self.add_error('phone_number', "Enter a valid phone number without the country code.")

            

#         if address is None:
#                     self.add_error('address', "Enter your address.")

            

#         return cleaned_data