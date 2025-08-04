from django.contrib.auth.forms import UserCreationForm as djangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as djangoUserChangeForm
from django import forms
from .models import User

class UserCreationForm(djangoUserCreationForm):
    class Meta:
        model = User
        # fields = ('email',)
        fields = ['email', 'password1', 'password2']
class UserChangeForm(djangoUserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
class ForgetPassword(forms.ModelForm):
    email = forms.EmailField(required=True)
    