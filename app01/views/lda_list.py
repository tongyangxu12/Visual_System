import json
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from app01 import models
from app01.models import csvdata_delete
from app01.utils.form import AnalysisModelForm
from app01.utils.pagination import Pagination
from LDA_Analysis.lda_analysis import analysis_find_k, lda_visual


BASE_DIR = os.getcwd()  # 获取当前文件路径 E:\Visual_System
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
RESULT = []

def lda_list(request):
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")
    queryset = models.CsvData.objects.all().order_by("id")
    page_object = Pagination(request, queryset)

    if request.method == "GET":
        form = AnalysisModelForm()

        context = {
            "form": form,
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html(),  # 生成页码
            "img_path": img_path
        }

        return render(request, "lda_list.html", context)

    form = AnalysisModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/lda/list/")

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "img_path": img_path
    }

    return render(request, "lda_list.html", context)


def lda_delete(request, nid):
    row_object = models.CsvData.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})


    models.CsvData.objects.filter(id=nid).delete()
    csvdata_delete(row_object)
    # filepath = row_object.data.file.name
    # print(filepath)
    #
    # os.remove(filepath)
    return redirect('/lda/list/')


def lda_analysis(request, nid):
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    data_path = models.CsvData.objects.filter(id=nid).values("data").first().get("data")
    global MEDIA_ROOT
    path = os.path.join(MEDIA_ROOT, data_path)

    if request.method == "GET":

        global RESULT
        RESULT = analysis_find_k(path)

        # RESULT = analysis(data_path)
        # print(type(RESULT[1]))
        # print(type(RESULT))


        return render(request, "lda_analysis.html", {"img_path": img_path})

    title = request.POST.get('title')
    lda_visual(path, int(title))
    # return redirect("/lda/list")
    return render(request, f"ldavis.html")



def chart_one(request):
    legend = []

    series_list = [
        {
            "type": 'line',
            "stack": 'Total',
            "data": RESULT[1]
        },
        # {
        #     "name": '上海',
        #     "type": 'line',
        #     "stack": 'Total',
        #     "data": [30, 40, 66, 20, 20, 100]
        # }
    ]

    x_axis = [i for i in RESULT[0]]

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }

    return JsonResponse(result)

