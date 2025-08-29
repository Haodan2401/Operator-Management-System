import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "details": forms.TextInput
        }

def task_list(request):
    queryset = models.Task.objects.all().order_by("-id")
    page_obj = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }

    return render(request, "task_list.html", context)

@csrf_exempt
def task_add(request):
    # 1.用户数据校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    data_dict = {"status": False, "error": form.errors}
    return JsonResponse(data_dict, json_dumps_params={"ensure_ascii": False})