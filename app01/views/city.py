import json
import os
import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django import forms
from django.conf import settings
from datetime import datetime



from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01.utils.pagination import Pagination

def city_list(request):
    if request.method == "GET":
        queryset = models.City.objects.all()
        return  render(request, "city_list.html", {"queryset": queryset})

class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"

def city_add(request):
    title = "Create City"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list")
    return render(request, "upload_form.html", {"form": form, "title": title})