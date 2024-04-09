"""
自定义的分页组件，以后如果想要使用这个分页组件，要做如下几件事：

在视图函数中：
    # 1.根据自己的情况去选择自己的数据，需要是queryset
    queryset = PrettyNum.objects.all().order_by("-level")

    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    # 通过实例化对象获得分完页的数据和生成的页码
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context={
        'queryset': page_queryset,  # 分完页的数据
        'page_string': page_string
    }
    return render(request, 'xxxx_list.html', context)

在HTML页面中：
    展示：
    {% for foo in queryset%}
        {{ foo.xxx }}
    {% endfor %}

    分页表：
    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe
import math
import copy

class Pagination:
     def __init__(self, request, queryset, page_param="page", page_size=10, inter=3):
         """
         :param request: 浏览器请求的对象
         :param queryset: 符合条件的数据（根据这个数据进行分页处理）
         :param page_param: 每页显示多少条数据
         :param page_size: 在url中传递的获取页数的参数，例如：/pretty/list/?page=11中的page
         :param inter: 显示当前页的前后几页（页码）
         """

         # 先深拷贝一份request.GET
         query_dict = copy.deepcopy(request.GET)
         # 修改query_dict的_mutable的值为True
         query_dict._mutable = True
         # 把query_dict设置为实例属性
         self.query_dict = query_dict

         self.page_param = page_param
         page = request.GET.get(page_param, "1")
         if page.isdecimal():
             page = int(page)
         else:
             page = 1
         self.page = page

         self.page_size = page_size

         self.start = (self.page - 1) * self.page_size
         self.end = self.page * self.page_size

         # page_queryset实例属性是执行完分页后的queryset
         # 所谓分页，无非就是把数据库查询到的queryset列表用切片的方式取一部分展示
         self.page_queryset = queryset[self.start:self.end]
         self.num = queryset.count()
         self.num_page = math.ceil(self.num/self.page_size)

         self.inter = inter

     def html(self):
         if self.num_page <= 2 * self.inter + 1:
             # 数据库的数据比较少，比2倍间隔还少，那么终止页只能是总页码数而不能是page+3
             start_page = 1
             end_page = self.num_page + 1 # 第二个1是因为range左闭右开
         else:
             # 数据库的数据比较多
             if self.page < self.inter + 1:
                 # page比较小的时候，起始页要是1，同时保证长度是2*inter，终止页也要改成2*inter+1
                 start_page = 1
                 end_page = 2 * self.inter + 1 + 1  # 第二个1是因为range左闭右开
             elif self.page + self.inter > self.num_page:
                 # page比较多，结束页要是总页码数，同时保证长度是2*inter，起始页也要修改
                 start_page = self.num_page - 2 * self.inter
                 end_page = self.num_page + 1  # 第二个1是因为range左闭右开
             else:
                 start_page = self.page - self.inter
                 end_page = self.page + self.inter + 1

         # 页码
         page_str_list = []

         # 首页
         self.query_dict.setlist(self.page_param, [1])
         first = f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>'
         page_str_list.append(first)

         # 创建上一页，要在for循环前面创建
         if self.page < 2:
             self.query_dict.setlist(self.page_param, [1])
             prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
         else:
             self.query_dict.setlist(self.page_param, [self.page - 1])
             prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
         page_str_list.append(prev)

         for i in range(start_page, end_page):
             self.query_dict.setlist(self.page_param, [i])
             if i == self.page:
                 ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
             else:
                 ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
             page_str_list.append(ele)

         # 创建下一页，要在for循环后面创建
         if self.page == self.num_page:
             self.query_dict.setlist(self.page_param, [self.num_page])
             next = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
         else:
             self.query_dict.setlist(self.page_param, [self.page + 1])
             next = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
         page_str_list.append(next)

         # 创建尾页，要在for循环后面、下一页后面创建
         self.query_dict.setlist(self.page_param, [self.num_page])
         last = f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>'
         page_str_list.append(last)

         # 所有的分页表已经完成，下面进行搜索框，也是把搜索框放到Pagination类里面，方便html文件
         search_string = """
                     <li>
                         <form style="float: left;margin-left: -1px" method="get">
                             <input name="page"
                                    style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                                    type="text" class="form-control" placeholder="页码">
                             <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                         </form>
                     </li>
                     """

         page_str_list.append(search_string)

         # 在page_str_list的所有值都整完后创建mark_safe
         page_string = mark_safe("".join(page_str_list))

         return page_string