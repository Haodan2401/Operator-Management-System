"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path, path
from django.views.static import serve
from django.conf import settings
from app01.views import depart, user, pretty, admin, account, task, order, chart, upload, city

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}, name="media"),

    # Department
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),
    path("depart/multi/", depart.depart_multi),

    # User
    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/model/form/add/", user.user_model_form_add),
    path("user/<int:nid>/edit", user.user_edit),
    path("user/<int:nid>/delete", user.user_delete),

    # Mobile
    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/<int:nid>/edit", pretty.pretty_edit),
    path("pretty/<int:nid>/delete", pretty.pretty_delete),

    # Admin
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/edit", admin.admin_edit),
    path("admin/<int:nid>/delete", admin.admin_delete),
    path("admin/<int:nid>/reset", admin.admin_reset),

    # Login
    path("login/", account.login),
    path("image/code/", account.image_code),
    path("logout/", account.logout),

    # Task
    path("task/list", task.task_list),
    path("task/add", task.task_add),

    # Order
    path("order/list/", order.order_list),
    path("order/add/", order.order_add),
    path("order/delete/", order.order_delete),
    path("order/edit/", order.order_edit),
    path("order/editPage/", order.order_editPage),

    # Chart
    path("chart/list/", chart.chart_list),
    path("chart/bar/", chart.chart_bar),
    path("chart/pie/", chart.chart_pie),
    path("chart/line/", chart.chart_line),

    # form
    path("upload/form/", upload.upload_form),
    path("upload/modal/form", upload.upload_modal_form),

    # City
    path("city/list/", city.city_list),
    path("city/add/", city.city_add),
]
