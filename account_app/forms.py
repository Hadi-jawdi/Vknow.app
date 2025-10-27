from django import forms
# from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# for registering user with email 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Save the email field
        if commit:
            user.save()
        return user

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)  # Adding the email field

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']  # Specify fields to include
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email '}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
#         }

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']  # Save the email field
#         if commit:
#             user.save()
#         return user




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