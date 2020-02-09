from django import forms
from django.contrib.auth import authenticate, login
import re
from django.core.exceptions import ValidationError
from .models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不对')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    def mobile_validate(value):
        mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
        if not mobile_re.match(value):
            raise ValidationError('手机号码格式错误')

    username = forms.CharField(label='用户名', max_length=30, min_length=4,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}))
    password = forms.CharField(label='密码', max_length=30, min_length=1,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))
    password_again = forms.CharField(label='再一遍密码', max_length=30, min_length=1,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '再来一次密码'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': '邮箱'}))
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': '验证码'}))
    mobile = forms.CharField(label='电话号码',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': '电话号码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已注册')

        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次密码不一致')

        return password_again



    def clean_code(self):
        v_code = self.cleaned_data.get('code', '').strip()
        if v_code == '':
            forms.ValidationError('验证码不能为空')
        return v_code

    def clean(self):
        v_code = self.request.session.get('email_verify_code', '')
        code = self.cleaned_data.get('code', '')

        if not (code == v_code and code != ''):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data




class EmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': '邮箱'}))
    code = forms.CharField(label='邮箱',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': '验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(EmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError('已经被绑定')
        return email

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('先登錄')

        if self.request.user.email != '':
            raise forms.ValidationError('已经绑定')

        v_code = self.request.session.get('email_verify_code', '')
        code = self.cleaned_data.get('code', '')
        if not (code == v_code and code != ''):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_code(self):
        v_code = self.cleaned_data('email_verify_code', '').strip()
        if v_code=='':
            forms.ValidationError('验证码不能为空')
        return v_code
