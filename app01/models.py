from django.db import models

# Create your models here.

class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="名称",max_length=32,unique=True)
    
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    # id = models.BigAutoField(verbose_name="ID",primary_key=True)
    # id = models.AutoField(verbose_name="ID",primary_key=True)
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="余额",max_digits=10,decimal_places=2,default=0)
    #create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    #depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE)
    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",null=True,blank=True,on_delete=models.SET_NULL)
    gender_choices = ((1,"男"),(2,"女"))
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

class Task(models.Model):
    """任务表"""
    level_choices = (
        (1,"紧急"),
        (2,"重要"),
        (3,"次要"),
    )
    number = models.CharField(verbose_name="任务号",max_length=64)
    title = models.CharField(verbose_name="标题",max_length=64)
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=1)
    detail = models.TextField(verbose_name="详细信息")

    director = models.ForeignKey(verbose_name="负责人",to="Admin",on_delete=models.CASCADE)
    #director = models.ForeignKey(verbose_name="负责人",to="Admin",null=True,blank=True,on_delete=models.SET_NULL)

class File(models.Model):

    detail = models.CharField(verbose_name="文件描述",max_length=64)
    file_path = models.CharField(verbose_name="文件路径",max_length=64)

class Image(models.Model):
    administrator = models.OneToOneField(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)
    image_path = models.FileField(verbose_name="图片路径",max_length=64,upload_to="img/")


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="账号",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    #外键默认引用
    def __str__(self):
        return self.username






    
