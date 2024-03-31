from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.modelform import ImageModelForm






def image_list(request):
    conditions_list = {}
    search = request.GET.get("search","")
    if search:
        conditions_list["administrator"] = search
    queryset = models.Image.objects.filter(**conditions_list).order_by("id")

    form = ImageModelForm()
    page_object = Pagination(request, queryset)
    context = {
        'search':search,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),       # 生成页码
        "form": form
        }
    return render(request, 'image_list.html', context)

def image_jump(request):
    return JsonResponse(request.GET)

def image_delete(request):
    uid = request.GET.get("uid")
    exists = models.Image.objects.filter(id=uid).exists()
    if not exists:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)
    models.Image.objects.filter(id=uid).delete()

    data_dict = {"status": True}
    return JsonResponse(data_dict)

@csrf_exempt
def image_add(request):
    form = ImageModelForm(data=request.POST,files=request.FILES)

    if form.is_valid():

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

def image_info(request):
    uid = request.GET.get("uid")
    exists = models.Image.objects.filter(id=uid).exists()
    if not exists:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)

    row_dict = models.Image.objects.filter(id=uid).values("administrator").first()
    data_dict = {
        "status": True,
        "data": row_dict
        }
    return JsonResponse(data_dict)

@csrf_exempt
def image_edit(request):
    uid = request.GET.get("uid")
    row_object = models.Image.objects.filter(id=uid).first()
    if not row_object:
        data_dict = {"status": False, "error": "id不存在"}
        return JsonResponse(data_dict)
    
    form = ImageModelForm(data=request.POST,files=request.FILES,instance=row_object)
    
    if not request.FILES:
            form.add_error("image_path","这个字段是必填项")
    if form.is_valid():
        form.save()

        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, "errors": form.errors}
    return JsonResponse(data_dict)
