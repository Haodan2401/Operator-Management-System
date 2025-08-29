import json
import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django import forms
from datetime import datetime

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination

def chart_list(request):
    return render(request, "chart_list.html")

def chart_bar(request):
    legend = ["Kris", "William"]
    series_list = [
        {
            "name": 'Kris',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": 'William',
            "type": 'bar',
            "data": [15, 10, 18, 5, 10, 30]
        }
    ]
    x_axis = ['Jan.', 'Feb.', 'March', 'April', 'May', 'June']
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)

def chart_pie(request):
    db_data_list = [
        {"value": 1140, "name": 'IT Department'},
        {"value": 735, "name": 'Sales Department'},
        {"value": 580, "name": 'Production Department'},
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)

def chart_line(request):
    legend = ["Shanghai", "Sichuan"]
    series_list = [
        {
            "name": 'Shanghai',
            "type": 'line',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": 'Sichuan',
            "type": 'line',
            "data": [15, 10, 18, 5, 10, 30]
        }
    ]
    x_axis = ['Jan.', 'Feb.', 'March', 'April', 'May', 'June']

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)