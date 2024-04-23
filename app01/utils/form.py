from app01 import models
from django import forms
from django.core.validators import RegexValidator  # 正则
from django.core.exceptions import ValidationError  # 错误信息
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm  # 自定义BootstrapModelForm类
from app01.utils.encrypt import md5

class UserResetModelForm(BootStrapModelForm):
    """重置管理员密码ModelForm"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('不能与以前的密码相同')

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class UserEditModelForm(BootStrapModelForm):

    class Meta:
        model = models.UserInfo
        fields = ['username']




class LoginForm(BootStrapForm):
    """登录ModelForm方法"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        required=True,  # 验证 必填，默认不能为空
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}, render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class AdminModelForm(BootStrapModelForm):
    """管理员的ModelForm方法"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm

    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exit = models.UserInfo.objects.filter(username=username)
        if is_exit:
            raise ValidationError("用户名已存在")

        return username


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["admin"]



class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.UserInfo
        fields = ["img"]


class AnalysisModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['data']
    class Meta:
        model = models.CsvData
        fields = '__all__'
        widgets = {
            'detail': forms.TextInput
        }



