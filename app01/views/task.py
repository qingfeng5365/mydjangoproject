import json
import random
from datetime import datetime

from app01 import models
from app01.utils.modelform import TaskModelForm
from app01.utils.pagination import Pagination
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt


def task_list(request):
    """任务列表"""
    
    conditions_list = {}
    search = request.GET.get("search","")
    if search:
        conditions_list["title__contains"] = search
    queryset = models.Task.objects.filter(**conditions_list).order_by("-id")
    #分页
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        'search':search,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),       # 生成页码
        "form": form,
        }
    return render(request, 'task_list.html', context)

def task_jump(request):

    return JsonResponse(request.GET)

@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.instance.number = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        form.instance.director_id = request.session["user_info"]["id"]
        form.save()
        data_dict = {"status": True}
        # json_string = json.dumps(data_dict)
        # return HttpResponse(json_string)
        return JsonResponse(data_dict)

    # data_dict = {"status": True,"errors": form.errors}
    # json_string = json.dumps(data_dict,ensure_ascii=False)
    # return HttpResponse(json_string)
    data_dict = {"status": False, "errors": form.errors}
    return JsonResponse(data_dict)

def task_delete(request):
    uid = request.GET.get("uid")
    exists = models.Task.objects.filter(id=uid).exists()
    if not exists:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)
    models.Task.objects.filter(id=uid).delete()
    data_dict = {"status": True}
    return JsonResponse(data_dict)

def task_info(request):
    uid = request.GET.get("uid")
    exists = models.Task.objects.filter(id=uid).exists()
    if not exists:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)

    row_dict = models.Task.objects.filter(id=uid).values("title","level","detail").first()
    data_dict = {
        "status": True,
        "data": row_dict
        }
    return JsonResponse(data_dict)

@csrf_exempt
def task_edit(request):
    uid = request.GET.get("uid")
    row_object = models.Task.objects.filter(id=uid).first()
    if not row_object:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)
    
    form = TaskModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, "errors": form.errors}
    return JsonResponse(data_dict)
       
"""
# 对象，当前行的所有数据。
row_object = models.Order.objects.filter(id=uid).first()
row_object.id
row_object.title
# 字典，{"id":1,"title":"xx"}
row_dict = models.Order.objects.filter(id=uid).values("id","title").first()
# queryset = [obj,obj,obj,]
queryset = models.Order.objects.all()
# queryset = [ {'id':1,'title':"xx"},{'id':2,'title':"xx"}, ]
queryset = models.Order.objects.all().values("id","title")
# queryset = [ (1,"xx"),(2,"xxx"), ]
queryset = models.Order.objects.all().values_list("id","title")
"""