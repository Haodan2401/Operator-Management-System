import json
import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django import forms
from datetime import datetime

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]

def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = OrderModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    # Ajax
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 只传了title, price, status, admin,缺少oid,admin
        # 额外增加用户未输入的值：订单号,管理员
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        form.instance.admin_id = request.session["info"]["id"]

        # 保存数据
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})

def order_delete(request):
    uid = request.GET.get("uid")
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "data not exists"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

# 展示Edit对话框并显示默认值
def order_edit(request):
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title","price","status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "data not exists"})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)

# 执行获取对象input数据并且更新数据库
@csrf_exempt
def order_editPage(request):
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "data not exists, please fresh page"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


