"""
所谓搜索，就是从数据库中获取到queryset列表里面通过切片获取有选择的数据
自定义的分页组件，以后如果想要使用这个分页组件，要做如下几件事：

在视图函数中：
    # 1.实例化搜索对象，需要传入的参数有request、要进行搜索的字段名(字符串类型)、去哪个数据表搜索的表名(这个表名不是简单的字符串类型，而是导入models.py里面的类)
    search_obj = Search(request, "username", Admin)

    # 2.通过实例化对象获得搜索关键字和搜索完的queryset
    search_data = search_obj.search_data
    queryset = search_obj.search()
    context={
        'queryset': page_queryset,  # 搜索完的数据(这个如果同时要实现分页功能,搜索的queryset作为参数传给分页做实例化对象)
        'search_data': search_data  # 搜索完成后在搜索框显示搜索关键字
    }
    return render(request, 'xxxx_list.html', context)

在HTML页面中：
    <form method="get">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Search for..." name="q" value="{{ search_data }}">  <!--一定要写name，因为这个是传给url参数的名称-->
                <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">  <!--想要用form提交，按钮必须是submit-->
                        <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
                    </button>
                </span>
        </div>
    </form>
"""
class Search:
    def __init__(self, request, field, table_name, search_param="q"):
        self.search_data = request.GET.get(search_param, '')
        self.field = field
        self.table_name = table_name
    def search(self):
        data_dict = {}
        if self.search_data:
            data_dict[self.field+"__contains"] = self.search_data
        queryset = self.table_name.objects.filter(**data_dict)

        return queryset