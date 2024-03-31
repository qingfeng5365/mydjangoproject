from django.shortcuts import render,redirect
from django.http import JsonResponse


from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.modelform import AdminModelForm,AdminEditModelForm,AdminResetModelForm

def admin_list(request):
    """管理员列表"""
    conditions_list = {}

    search = request.GET.get("search","")
    if search:
        conditions_list["username__contains"] = search
    queryset = models.Admin.objects.filter(**conditions_list).order_by("id")
   
    #分页
    page_object = Pagination(request, queryset)
    context = {
        'search':search,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()       # 生成页码
        }
    return render(request, 'admin_list.html', context)

def admin_jump(request):
    
    return JsonResponse(request.GET)

def admin_add(request):
    """新建管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,'change.html',{"form":form,"title":title})
    
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,'change.html',{"form":form,"title":title})

def admin_edit(request,nid):
    """编辑管理员"""
    title = "编辑管理员"
    row_object = models.Admin.objects.filter(id=nid).first()
    if request.method == "GET":

        if not row_object:
            error = "id不存在"
            return render(request,"error.html",{"error":error})
            
        form = AdminEditModelForm(instance=row_object)
        return render(request,'change.html',{"form":form,"title":title})
    
    form = AdminEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,'change.html',{"form":form,"title":title})

def admin_delete(request,nid):
    """删除部门"""
    exists = models.Admin.objects.filter(id=nid).exists()
    if not exists:
        error = "id不存在"
        return render(request,"error.html",{"error":error})
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

def admin_reset(request,nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    title = "重置密码 - {}".format(row_object.username)
    if request.method == "GET":

        if not row_object:
            error = "id不存在"
            return render(request,"error.html",{"error":error})
            
        form = AdminResetModelForm()
        return render(request,'change.html',{"form":form,"title":title})
    
    form = AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request,'change.html',{"form":form,"title":title})

