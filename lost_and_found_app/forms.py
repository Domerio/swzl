import re
from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'real_name', 'role', 'phone', 'avatar']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 假设学号/工号是数字，长度为8 - 12位
        if not re.match(r'^\d{8,12}$', username):
            raise forms.ValidationError("学号/工号格式不正确，请输入8 - 12位数字。")
        return username

    def clean_password2(self):
        # 检查两次输入的密码是否一致
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致")
        return password2

    def save(self, commit=True):
        # 保存用户信息并设置密码
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
