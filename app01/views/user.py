from django.shortcuts import render,redirect
from django.http import JsonResponse
                                        

from app01 import models
from app01.utils.modelform import UserModelForm,UserEditModelForm
from app01.utils.pagination import Pagination

def user_list(request):
    """用户列表"""
    '''
    models.UserInfo.objects.filter(id=12)
    models.UserInfo.objects.filter(id__gt=12)
    models.UserInfo.objects.filter(id__gre=12)
    models.UserInfo.objects.filter(id__lt=12)
    models.UserInfo.objects.filter(id__lte=12)

    models.UserInfo.objects.filter(name__contains="张")
    models.UserInfo.objects.filter(name__startwith="张")
    models.UserInfo.objects.filter(name__endwith="张")
    '''
    conditions_list = {}
    search = request.GET.get("search","")
    if search:
        conditions_list["name__contains"] = search
    queryset = models.UserInfo.objects.filter(**conditions_list).order_by("id")
    #for obj in queryset:
        #("%Y-%m-%d-%H-%M")
        #print(obj.id,obj.name,obj.password,obj.age,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.gender,obj.get_gender_display(),obj.depart.title)

    #分页
    page_object = Pagination(request, queryset)
    context = {
        'search':search,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()       # 生成页码
        }
    #return render(request,'user_list.html',{'queryset':queryset,'search':search})
    return render(request, 'user_list.html', context)

def user_jump(request):

    return JsonResponse(request.GET)

def user_add(request):
    """新建用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request,'user_add.html',{"form":form})
    
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        #print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    #print(form.errors)
    return render(request,'user_add.html',{"form":form})
    
def user_edit(request,nid):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        
        if not row_object:
            error = "id不存在"
            return render(request,"error.html",{"error":error})
        form = UserEditModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})

    form = UserEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #print(form.cleaned_data)
        #form.instance.password="qqq"
        form.save()
        return redirect("/user/list/")
    #print(form.errors)
    return render(request,'user_edit.html',{"form":form})

def user_delete(request,nid):
    exists = models.UserInfo.objects.filter(id=nid).exists()
    if not exists:
        error = "id不存在"
        return render(request,"error.html",{"error":error})

    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
