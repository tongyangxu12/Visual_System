from django.shortcuts import render
from django.http import JsonResponse
from app01.models import DataCsv


def analysis_sentiment(request, nid):
    row_obj = DataCsv.objects.filter(id=nid).first()


def analysis_cluster(request):
    pass


def analysis_lda(request):
    pass