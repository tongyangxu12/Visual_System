"""
csv数据 视图函数
"""
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import DataModelForm


def data_list(request):
    """城市列表"""
    queryset = models.DataCsv.objects.all()
    return render(request, 'data_list.html', {'queryset': queryset})


def data_add(request):
    """添加城市"""
    if request.method == 'GET':
        form = DataModelForm
        return render(request, 'data_add.html', {'form': form})

    form = DataModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/data/list/')
    return render(request, 'data_add.html', {'form': form})


