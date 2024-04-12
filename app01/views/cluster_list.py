import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AnalysisModelForm
from app01.models import csvdata_delete
from Cluster_Analysis.cluster_analysis import analysis

BASE_DIR = os.getcwd()  # 获取当前文件路径 E:\Visual_System
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CSV_PATH = ""


def cluster_list(request):
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

        return render(request, "cluster_list.html", context)

    form = AnalysisModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/cluster/list/")

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "img_path": img_path
    }

    return render(request, "cluster_list.html", context)


def cluster_delete(request, nid):
    row_object = models.CsvData.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    models.CsvData.objects.filter(id=nid).delete()
    csvdata_delete(row_object)
    return redirect('/cluster/list/')


def cluster_analysis(request, nid):
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    if request.method == "GET":
        data_path = models.CsvData.objects.filter(id=nid).values("data").first().get("data")
        global MEDIA_ROOT
        global CSV_PATH
        CSV_PATH = os.path.join(MEDIA_ROOT, data_path)

        # RESULT = analysis(data_path)
        # print(type(RESULT[1]))
        # print(type(RESULT))


        return render(request, "cluster_analysis.html", {"img_path": img_path})



def chart_one(request):

    data = analysis(CSV_PATH, 2)
    result = {
        "status": True,
        "data": data

    }
    return JsonResponse(result)



def chart_two(request):
    data = analysis(CSV_PATH, 3)
    result = {
        "status": True,
        "data": data

    }
    return JsonResponse(result)


def chart_three(request):
    data = analysis(CSV_PATH, 4)
    result = {
        "status": True,
        "data": data

    }
    return JsonResponse(result)


def chart_four(request):
    data = analysis(CSV_PATH, 5)
    result = {
        "status": True,
        "data": data

    }
    return JsonResponse(result)