"""
自定义的分页组件，以后如果想要使用，需要做如下几件事：

在视图函数中：
def pretty_list(request):
    # 1.根据自己的情况取筛选自己的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level") # 取出电话号码里包含136的所有对象

    # 2. 实例化分页的对象
    page_object = Pagination(request, queryset) #创建类的实例

    context = {
        "queryset": page_object.page_queryset, # 摘取出当前页应该展示的所有对象
        "page_string": page_object.html() # 形成当前页码的html文件
    }
    return render(request, "pretty_list.html", context)

在HTML页面中：

    {% for obj in queryset %}
        {{ obj.xx }}
    {% endfor %}


    <ul class="pagination">
        {{ page_string }}
    </ul>

"""


from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy

class Pagination:
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable_ = True
        self.query_dict = query_dict
        self.page_param = page_param


        page = request.GET.get(page_param, "1") # 获取前端给到的页数
        if page.isdecimal():
            page = int(request.GET.get(page_param, "1"))
        else:
            page = "1"
        self.page = page # int: 页数
        self.page_size = page_size

        self.start = (page - 1) * page_size # 取当前页的第一个对象
        self.end = page * page_size # 取当前页的最后一个对象

        self.page_queryset = queryset[self.start:self.end] # 摘取出当前页应该展示的所有对象

        total_count = queryset.count() # 整个search出来的所有对象个数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count # 所有页数
        self.plus = plus # 页数间隔，比如plus=5，那么点击20则显示15-25页

    def html(self):
        # 处理edge cases，例如页面小于plus等
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 创建数组承装字符串，等待最后合并
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">Head</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        num = max(1, self.page - 1)
        self.query_dict.setlist(self.page_param, [num])
        page_str_list.append('<li><a href="?{}">«</a></li>'.format(self.query_dict.urlencode()))

        # 中间页面组
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        num = min(self.page + 1, self.total_page_count)
        self.query_dict.setlist(self.page_param, [num])
        page_str_list.append('<li><a href="?{}">»</a></li>'.format(self.query_dict.urlencode()))

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">Tail</a></li>'.format(self.query_dict.urlencode()))

        # 跳转窗
        search_string = """
            <li>
                <form style="float: left; margin-left: -1px" method="GET">
                    <input name="page"
                           style="position: relative;float:left;display: inline-block;width:80px"
                           type="text" class="form-control" placeholder="page">
                    <button style="border-radius:0" class="btn btn-default"  type="submit">jump</button>
                </form>
            
            </li>
        """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string