from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout

import random
import string
import time
from django.conf import settings
from .forms import LoginForm,RegisterForm,EmailForm
from .models import MyUser
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError
def user_login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
        return render(request, 'login.html', {'form': loginForm})
    else:

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user=login_form.cleaned_data['user']
            login(request, user)
            if request.POST.get('path') == '':
                return redirect(reverse('home'))
            else:
                return redirect(request.POST.get('path'))

        else:
            loginForm = LoginForm(request.POST)
            return render(request, 'login.html', {'form': loginForm})

def user_regsier(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
        return render(request, 'register.html', {'form': registerForm})
    else:
        registerForm = RegisterForm(request.POST,request=request)
        if registerForm.is_valid():
            user=MyUser.objects.create_user(username=registerForm.cleaned_data['username'],password=registerForm.cleaned_data['password'],
                                       mobile=registerForm.cleaned_data['mobile'],email=registerForm.cleaned_data['email'])
            login(request,user)
            del request.session['email_verify_code']
            if request.POST.get('path')=='':
                return redirect(reverse('home'))
            else:
                return redirect(request.POST.get('path'))
        else:

            return render(request, 'register.html', {'form': registerForm})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def login_from_modal(request):
    login_form=LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        login(request, user)
        data={}
        data['status']='SUCCESS'
        return JsonResponse(data)
    else:
        data = {}
        data['ERROR'] = 'ERROR'
        return JsonResponse(data)

def get_user_info(request):
    if request.user.is_authenticated:
        return render(request,'user_info.html')
    else:
        return redirect(reverse('common:login'))

def change_email(request):
    if request.method=='GET':
        emailForm=EmailForm()
        return render(request,'change_email.html',{'form':emailForm})
    else:
        form=EmailForm(request.POST,request=request)
        if form.is_valid():
            user=request.user
            user.email=form.cleaned_data['email']
            user.save()
            del request.session['email_verify_code']
            return redirect(reverse('common:get_user_info'))
        else:
            return render(request,'change_email.html',{'form':form})



def send_email_verify_code(request):
    data={}
    email=request.GET.get('email_address')

    if email!='':
        code=''.join(random.sample(string.ascii_lowercase+string.digits,4))
        request.session['email_verify_code']=code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now-send_code_time<30:
            data['status']='ERROR'
        else:
            message = '验证码：'+code
            send_mail('绑定邮箱', message, 'gh632830515@126.com', [email], fail_silently=False)
            data['status']='SUCCESS'
            data['send_code_time']=int(time.time())

    else:
        data['status']='ERROR'
    return JsonResponse(data)