import os

from app01 import models
from app01.utils.modelform import FileForm
from app01.utils.pagination import Pagination
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render


def file_list(request):

    """头像列表"""
    
    conditions_list = {}
    search = request.GET.get("search","")
    if search:
        conditions_list["detail__contains"] = search
    queryset = models.File.objects.filter(**conditions_list).order_by("-id")
    #分页
    page_object = Pagination(request, queryset)
    context = {
        'search':search,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),       # 生成页码
        }
    return render(request,"file_list.html", context)

def file_jump(request):
    return JsonResponse(request.GET)

def file_add(request):
    """新建文件"""
    if request.method == "GET":
        form = FileForm()
        return render(request,'file_add.html',{"form":form})
    
    form = FileForm(data=request.POST,files=request.FILES)

    if form.is_valid():
        file_object = form.cleaned_data.get("file")
        #print(form.cleaned_data)

        file_path = os.path.join("media","file",file_object.name)
        #print(file_path)
        with open(file_path,mode="wb") as f:
            for chunk in file_object.chunks():
                f.write(chunk)

        models.File.objects.create(
            detail = form.cleaned_data["detail"],
            file_path = file_path
        )
        return redirect("/file/list/")

    return render(request,'file_add.html',{"form":form})

def file_edit(request,nid):
    """编辑文件"""
    if request.method == "GET":
        exists = models.File.objects.filter(id=nid).exists()
        if not exists:
            error = "id不存在"
            return render(request,"error.html",{"error":error})
        row_object = models.File.objects.filter(id=nid).first()
        return render(request,'file_edit.html',{'row_object':row_object})
    detail = request.POST.get("detail")
    if detail == "":
        error = "描述不能为空"
        return render(request,'error.html',{"error":error})
    exists = models.File.objects.exclude(id=nid).filter(detail=detail).exists()
    if exists:
        error = "描述已存在"
        return render(request,'error.html',{"error":error})
    if detail==models.File.objects.filter(id=nid).first().detail:
        return redirect("/file/list/")
    models.File.objects.filter(id=nid).update(detail=detail)
    return redirect("/file/list/")


def file_delete(request):
    """删除部门"""
    nid = request.GET.get("nid")
    exists = models.File.objects.filter(id=nid).exists()
    if not exists:
        error = "id不存在"
        return render(request,"error.html",{"error":error})
    models.File.objects.filter(id=nid).delete()
    return redirect("/file/list/")
