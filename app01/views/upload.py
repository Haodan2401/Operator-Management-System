import json
import os
import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django import forms
from django.conf import settings
from datetime import datetime



from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01.utils.pagination import Pagination

class UpForm(BootStrapForm):
    name = forms.CharField(label="name")
    age = forms.IntegerField(label="age")
    img = forms.FileField(label="img")

def upload_form(request):
    title = "Upload Form"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        img_object = form.cleaned_data.get("img")
        # file_path = os.path.join(settings.MEDIA_ROOT, img_object.name)
        file_path = os.path.join("media", img_object.name)
        f = open(file_path, mode="wb")
        for chunks in img_object.chunks():
            f.write(chunks)
        f.close()

        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=file_path,
        )

        return HttpResponse("...")
    return render(request, "upload_form.html", {"form": form, "title": title})


class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"

def upload_modal_form(request):
    title = "Upload Model Form"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("success")