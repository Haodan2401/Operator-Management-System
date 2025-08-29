from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0. 排除不需要过中间件就能访问的页面
        if request.path_info in ["/image/code/", "/login/"]:
            return

        # 1. 查看服务器session中是否有当前访问用户的信息，如果已登陆就往后走
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2. 服务器session没有查到，未登陆，重新返回登陆界面
        return redirect("/login/")