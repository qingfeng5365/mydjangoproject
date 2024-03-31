from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, TextInput

from app01 import models
from app01.utils.encrypt import md5

class BootStrap:
    bootstrap_exclude_fields = []
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for col_name,field in self.fields.items():
            if col_name == "":
                continue
            if col_name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                #原先有值，保留原先的值，并添加新值           
                field.widget.attrs["class"]="form-control"
                field.widget.attrs["placeholder"]=field.label
                #pass
            else:
                #原先没有值，添加
                field.widget.attrs = {"class":"form-control","placeholder":field.label,}

class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass

class BootStrapForm(BootStrap,forms.Form):
    pass

class UserModelForm(BootStrapModelForm):
    #xx = forms.CharField(widget=forms.Input)
    #验证方式1：正则
    password = forms.CharField(widget=forms.PasswordInput(attrs={}),min_length=6,label="密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        # exclude = ['name']
        fields = ["name","password","age","account","create_time","gender","depart"]
        widgets = {
            #"password": forms.PasswordInput(attrs={})
            #"create_time": forms.TextInput(attrs={"id":"dt",})
            }
        
    #验证方式2：钩子
    def clean_age(self):
        txt_age = self.cleaned_data["age"]
        if txt_age < 10:
            raise ValidationError("年龄不能低于10周岁")
        return txt_age
    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists = models.UserInfo.objects.filter(name=txt_name).exists()
        if exists:
            raise ValidationError("姓名已存在")
        return txt_name

class UserEditModelForm(BootStrapModelForm):
    #xx = forms.CharField(widget=forms.Input)
    account = forms.CharField(disabled=True,label="余额")
    #验证方式1：正则
    password = forms.CharField(widget=forms.PasswordInput,min_length=6,label="密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        # exclude = ['name']
        fields = ["name","password","age","account","create_time","gender","depart"]
        widgets = {
            #"password": forms.PasswordInput(attrs={})
            #"create_time": forms.TextInput(attrs={"id":"dt",})
            }

    #验证方式2：钩子
    def clean_age(self):
        txt_age = self.cleaned_data["age"]
        if txt_age < 10:
            raise ValidationError("年龄不能低于10周岁")
        return txt_age
    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists = models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exists:
            raise ValidationError("姓名已存在")
        return txt_name

class AdminModelForm(BootStrapModelForm):
    #验证方式1：正则
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),min_length=6,label="密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={},render_value=True),min_length=6,label="确认密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            #"password": forms.PasswordInput(attrs={})
            #"create_time": forms.TextInput(attrs={"id":"dt",})
            }
        

    #验证方式2：钩子
    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.Admin.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("账户已存在")
        return username

    def clean_password(self):
        pwd= self.cleaned_data["password"]
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]
    #验证方式2：钩子
    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(username=username).exists()
        if exists:
            raise ValidationError("账户已存在")
        return username

class AdminResetModelForm(BootStrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),min_length=6,label="密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={},render_value=True),min_length=6,label="确认密码",validators=[RegexValidator(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',"密码至少包含数字和字母，长度6-20")])
    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("重置密码不能与原来密码一致")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd and pwd:
            raise ValidationError("密码不一致")
        return confirm
    
class LoginForm(BootStrapForm):
    username = forms.CharField(widget=forms.TextInput(),label="账户",required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),label="密码",required=True)
    img_code = forms.CharField(widget=forms.TextInput(),label="图片验证码",required=True)

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        #fields = "__all__"
        exclude = ['number','director']
        widgets = {
            "detail": forms.TextInput
            #"detail": forms.Textarea,
        }

class FileForm(BootStrapForm):
    bootstrap_exclude_fields = ['file']
    detail = forms.CharField(label="文件描述")
    file = forms.FileField(label="文件路径")

class ImageModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['image_path']
    class Meta:
        model = models.Image
        fields = "__all__"
        widgets = {
            #"image_path": forms.FileInput
            #"detail": forms.Textarea,
        }
