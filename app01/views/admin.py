from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination


def admin_list(request):
    """ Admin List """
    # info_dict = request.session["info"]
    # print(info_dict)


    data_dict = {}
    search_data = request.GET.get('q', "")   # 你输入的想要查找的数据，比如这里输入框里填写的"136"..获取到"136"
    if search_data:
        data_dict["username__contains"] = search_data  # 电话号码里包含136

    queryset = models.Admin.objects.filter(**data_dict)
    page_obj = Pagination(request, queryset, page_size=2)

    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html,
        "search_data": search_data
    }
    return render(request, "admin_list.html", context)




from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))

        if confirm != pwd:
            raise ValidationError("Password not the same!")
        # 返回什么，此字段以后保存在数据库就是什么（会覆盖用户输入的值）
        return confirm


def admin_add(request):
    """ add admin """
    title = "Create Admin"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 因为Django会在form.is_valid()的执行过程中自动发现并调用所有以clean_<fieldname>命名的方法。
        # Django执行is_valid步：
        # 1. 先进行基本的字段验证（是否为空，长度等）
        # 2. 然后将验证好的数据放进cleaned data中，
        # 3. 然后再自动调用自定义的钩子函数进行再验证
        form.save()
        return redirect("/admin/list")
    else:
        return render(request, "change.html", {"form": form, "title": title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    msg = "data not exists"
    if not row_object:
        # return render(request, "error.html", {"msg": msg})
        return redirect("/admin/list")

    title = "Edit Admin"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    msg = "data not exists"
    if not row_object:
        # return render(request, "error.html", {"msg": msg})
        return redirect("/admin/list")

    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list")



class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("Passwaord cannot be the same as before!")

        return md5_pwd

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))

        if confirm != pwd:
            raise ValidationError("Password not the same!")
        # 返回什么，此字段以后保存在数据库就是什么（会覆盖用户输入的值）
        return confirm

def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    msg = "data not exists"
    if not row_object:
        # return render(request, "error.html", {"msg": msg})
        return redirect("/admin/list")

    title = "reset password - {}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})
