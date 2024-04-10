import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from app01 import models
from app01.utils.form import SentimentModelForm
from app01.utils.pagination import Pagination
from Sentiment_Analysis.sentiment_analysis import analysis


BASE_DIR = os.getcwd()  # 获取当前文件路径 E:\Visual_System
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
RESULT = ()
def sentiment_list(request):

    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")
    queryset = models.CsvData.objects.all().order_by("id")
    page_object = Pagination(request, queryset)

    if request.method == "GET":
        form = SentimentModelForm()

        context = {
            "form": form,
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html(),  # 生成页码
            "img_path": img_path
        }

        return render(request, "sentiment_list.html", context)

    form = SentimentModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/sentiment/list/")

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "img_path": img_path
    }

    return render(request, "sentiment_list.html", context)



def sentiment_delete(request, nid):
    row_object = models.CsvData.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    models.CsvData.objects.filter(id=nid).delete()
    return redirect('/sentiment/list/')


def sentiment_analysis(request, nid):
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    if request.method == "GET":
        data_path = models.CsvData.objects.filter(id=nid).values("data").first().get("data")
        global MEDIA_ROOT
        global BASE_DIR
        global RESULT
        data_path = os.path.join(MEDIA_ROOT, data_path)

        RESULT = analysis(data_path)
        print(type(RESULT[1]))
        print(type(RESULT))
        return render(request, "sentiment_analysis.html", {"img_path": img_path})


def chart_one(request):
    # analysis()  # 传入数据
    legend = []  #

    series_list = [
        # 获得的数据
        {
            "type": 'line',
            "stack": 'Total',
            "data": RESULT[1]
        },
        """
        {
            "name": '河北',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 100]
        },
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [30, 40, 66, 20, 20, 100]
        }
        """
    ]

    x_axis = [item for item in range(len(RESULT[1]))]  # 获得的数据

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)



def chart_two(request):
    data_list = [
        { "value": RESULT[0][2], "name": '消极' },
        { "value": RESULT[0][1], "name": '中性' },
        { "value": RESULT[0][0], "name": '积极' },

      ]
    result = {
        "status": True,
        "data": data_list,
        'subtext': "好评率:%.2f%%" % RESULT[2]
    }
    print("RESULT[2]:", RESULT[2])
    return JsonResponse(result)


def chart_three(request):

    series_list = [
        {
            "type": 'bar',
            "data": RESULT[3][1]
        },
        """
        {
            "name": '萧炎',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 100]
        },
        {
            "name": '美杜莎',
            "type": 'bar',
            "data": [30, 40, 66, 20, 20, 100]
        }
        """
    ]

    x_axis = RESULT[3][0]

    result = {
        "status": True,
        "data": {
            "series_list": series_list,
            "x_axis": x_axis,
            "text": RESULT[3][2]
        }
    }

    return JsonResponse(result)