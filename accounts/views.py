

# Create your views here.
from django.shortcuts import redirect, render
from django.views import View
from accounts.forms import UserRegistrationForm, UserLoginForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages


# Login
class UserLoginView(View):
    username = []
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('search:search_google')
        else:
            greeting={}
            greeting['form'] = UserLoginForm
            return render(request, 'auth-login.html', greeting)

    def post(self,request):
        if(request.method == "POST"):
            username = request.POST.get('username')
            password = request.POST.get('password')

            if(username != '' and password != ''):
                user = auth.authenticate(username=username, password=password)
                if user is not None:       
                    auth.login(request, user)
                    UserLoginView.username.append(username)
                    data={}
                    data['success_message'] ='Successfully login'
                    return redirect('accounts:auth-login')
                 
                else:
                    data={}
                    data['error_message'] ='Invalid Credentials'
                    messages.add_message(request, messages.SUCCESS, 'Invalid Credentials')
                    return redirect('accounts:auth-login')
               
            else:
                data={}
                data['error_message'] ='Some field is empty'
                messages.add_message(request, messages.WARNING, 'Some field is empty')
                return redirect('accounts:auth-login')
        else:
            return redirect('accounts:auth-login')

# Registration
class UserRegisterView(View):
    def get(self,request):
        greeting={}
        greeting['form'] = UserRegistrationForm
        if request.user.is_authenticated:
            return redirect('search:search_google')
        auth.logout(request)
        return render(request,'accounts:auth-register.html',greeting)
    def post(self,request):
        if request.method == "POST":
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            password1 = request.POST.get('password2')
            # print(email, username, password, password1)
            
            if(email != '' and username != '' and password != '' and password1 != '' ):
                
                if User.objects.filter(username=username).exists():
                    print(email, 'user')
                  
                    data={}
                    data['error_message'] = 'Username Is Already Exists'
                    messages.add_message(request, messages.INFO, 'Username Is Already Exists')
                    
                    return redirect('accounts:auth-register')
                elif User.objects.filter(email=email).exists():
                    print(email, 'email')
                    data={}
                    data['error_message'] ='Email Is Already Exists'
                    messages.add_message(request, messages.INFO, 'Email Is Already Exists')
                    return redirect('accounts:auth-register')
                elif(password == password1):
                    print(email, 'password')
                    form = UserRegistrationForm(request.POST)
                    if form.is_valid():
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        data={'success_message' : "Successfully registered please login"}
                        messages.add_message(request, messages.SUCCESS, 'Successfully registered please login.')
                        return redirect('accounts:auth-register')
                else:
                    print(email, 'password not match')
                    data={}
                    data['error_message'] ='password and confirm password is not match'
                    messages.add_message(request, messages.INFO, 'password and confirm password is not match')
                    return redirect('accounts:auth-register')
            else:
                data={}
                data['error_message'] ='Some field is empty'
                messages.add_message(request, messages.WARNING, 'Some field is empty')
                return redirect('accounts:auth-register')
        else:
            return redirect('accounts:auth-login')


def logout(request):
    auth.logout(request)
    return redirect('accounts:auth-login')



def deshBoard(request):
    print('hello')
    return render(request, 'Deshboard.html',{'message':'hello'} )