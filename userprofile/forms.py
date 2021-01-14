# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User

# 登录表单，继承了forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()