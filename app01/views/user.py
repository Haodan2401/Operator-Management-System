from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


############## User Form ####################
def user_list(request):
    """ User List"""
    queryset = models.UserInfo.objects.all()
    page_obj = Pagination(request, queryset, page_size=5)

    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html,
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """ Add User """
    if request.method == "GET":
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    savings = request.POST.get("savings")
    ctime = request.POST.get("ctime")
    gender = request.POST.get("gender")
    depart_id = request.POST.get("dp")

    models.UserInfo.objects.create(name=name, password=pwd, age=age, savings=savings,
                                   create_time=ctime, gender=gender, depart_id=depart_id)

    return redirect("/user/list/")


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 对POST进行数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect("/user/list")
    else:
        return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """ edit user """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    else:
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect("/user/list")
        else:
            return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ delete user """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')