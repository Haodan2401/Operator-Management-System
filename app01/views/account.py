from django.shortcuts import render,redirect,HttpResponse
from django import forms

from io import BytesIO

from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.picture import generate_captcha
from app01 import models


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="code",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)



def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # admin_obj = models.Admin.objects().filter(username="",password="").first()

        # 验证码校验
        user_input_code = form.cleaned_data.pop("code") #获取的是用户输入的验证码
        random_code = request.session.get("image_code", "") #获取的是随机生成的验证码

        if random_code.upper() != user_input_code.upper():
            form.add_error("code", "Code is incorrect")
            return render(request, "login.html", {"form": form})

        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "Username or password is incorrect")
            return render(request, "login.html", {"form": form})

        # 验证成功
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到服务器(Django默认mysql)的session中
        request.session["info"] = {"id":admin_obj.id, "name":admin_obj.username}
        request.session.set_expiry(60 * 60 * 24 * 7) # 七天免登陆
        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})

def image_code(request):
    img, code_string = generate_captcha()
    print(f"验证码文本: {code_string}")

    # 写入用户的session以便校验
    request.session["image_code"] = code_string
    # 设定六十秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()
    return redirect("/login/")