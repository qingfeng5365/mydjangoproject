from io import BytesIO

from django.shortcuts import render,redirect,HttpResponse

from app01 import models
from app01.utils.modelform import LoginForm
from app01.utils.check_code import check_code

def login(request):
    """登录"""
    if request.session.get("user_info"):
            return redirect("/admin/list/")
    if request.method=="GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        img_code_input = form.cleaned_data.pop("img_code")
        img_code = request.session.get("img_code","")
        if not img_code:
            form.add_error("img_code","验证码已过期")
            return render(request,"login.html",{"form":form})

        if img_code_input.upper() != img_code.upper():
            form.add_error("img_code","验证码错误")
            return render(request,"login.html",{"form":form})

        row_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not row_object:
            form.add_error("password","用户名/密码错误")
            return render(request,"login.html",{"form":form})


        request.session.clear()
        request.session["user_info"] = {'id':row_object.id,'username':row_object.username}
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")
    return render(request,"login.html",{"form":form})

def image_code(request):
    """图片验证码"""

    if request.session.get("user_info"):
        return redirect("/admin/list/")

    img,code_string = check_code()

    request.session["img_code"] = code_string
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()
    return redirect("/login/")
    