from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
# from.forms import UserProfileForm
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from django.http import HttpResponse


#for sending email to user when user is registering 
def test_email(request):
    subject = 'Test Email from Django'
    message = 'This is a test email to confirm your email setup in Django.'
    from_email = 'Hadijawadi1385@gmail.com'  # Replace with your email address
    recipient_list = ['hadi.jawdi2006@gmail.com']  # Replace with the recipient's email address

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Failed to send email: {e}')


def login_user(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password  = request.POST['password']
        user = authenticate(username = username , password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'account_app/pages/login.html',{'error':'Invalid username or password'})
    return render(request,'account_app/pages/login.html')

def register_user(request):
    if request.method == 'POST':
         form = CustomUserCreationForm(data= request.POST)
         if form.is_valid():
             new_user = form.save()
             user_email = form.cleaned_data['email']  # Access the email from cleaned_data

              # Send the welcome email
            #  send_mail(
            #     'Thank You for Registering ',
            #     'Welcome! Thank you for registering on our Website. We are excited to have you. developerTeam (YDL)',
            #     'hadijawadi1385@gmail.com',
            #     [user_email],
            #     fail_silently=False,
            #   )
            #  login(request,new_user)
             return redirect('home')
    form =CustomUserCreationForm()
    context= {
        'form':form
    }
    return render(request,'account_app/pages/register.html',context)


def dashboard(request):

    return render(request, "account_app/pages/dashboard.html")
    
from django.contrib.auth import logout


def logout_user(request):
    logout(request)
    return redirect('home')  # or wherever you want