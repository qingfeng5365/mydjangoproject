from app01 import models
from app01.utils.modelform import ImageModelForm

from django.http import JsonResponse


def avatar_get(request):
    admin_id = request.session["user_info"].get("id")
    row_object = models.Image.objects.filter(administrator=admin_id).first()
    image_path = str(row_object.image_path)
    data_dict = {"image_path": image_path}
    return JsonResponse(data_dict)
