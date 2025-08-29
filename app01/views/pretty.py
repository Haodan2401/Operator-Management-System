from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, PrettyAddModelForm, PrettyEditModelForm

############## Mobile Form ####################

def pretty_list(request):
    """ Mobile List """
    data_dict = {}
    search_data = request.GET.get('q', "")   # 你输入的想要查找的数据，比如这里输入框里填写的"136"..获取到"136"
    if search_data:
        data_dict["mobile__contains"] = search_data  # 电话号码里包含136

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level") # 取出电话号码里包含136的所有对象

    page_object = Pagination(request, queryset) #创建类的实例

    context = {
        "search_data": search_data, # 你输入的想要查找的数据，比如这里输入框里填写的"136"..获取到"136"
        "queryset": page_object.page_queryset, # 摘取出当前页应该展示的所有对象
        "page_string": page_object.html() # 形成当前页码的html文件
    }
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """ Mobile ADD """
    if request.method == "GET":
        form = PrettyAddModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 对POST进行数据校验
    form = PrettyAddModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/pretty/list")
    else:
        return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """ edit number """
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    else:
        form = PrettyEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect("/pretty/list")
        else:
            return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """ delete user """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')