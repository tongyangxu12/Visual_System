import os
import csv
import time
import random
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.http import FileResponse

from app01 import models
from Spider_JD.spider import get_content


FLAG = 0

def spider_list(request):
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    # os.chdir(os.path.join(os.getcwd(), "spider_comment"))
    # print(os.getcwd())

    context = {
        "img_path": img_path
    }

    if request.method == "GET":

        return render(request, "spider_list.html", context)

    product_id = request.POST.get('title')
    page_number = request.POST.get('page')
    print(product_id)
    print(page_number)
    path = os.path.join(os.getcwd(), "spider_comment")
    with open(os.path.join(path, f"JD_comment.csv"), 'w', encoding='utf_8_sig') as f:

        print("打开了！")
        csvwriter = csv.writer(f)
        csvwriter.writerow(('评分', '评论时间', '评论内容'))

        for page in range(int(page_number)):
            print("开始for")
            try:
                print("开始try")

                # 目标网址
                url = 'https://club.jd.com/comment/productPageComments.action'
                # 参数
                params = {
                    'productId': product_id,
                    'score': 0,
                    'sortType': 5,
                    'page': page,
                    'pageSize': 10,
                    'isShadowSku': 0,
                    'fold': 1
                }
                # 请求头
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                    'cookie': '__jdu=1840732391; shshshfpa=f9136121-78e7-0947-12fc-9805261422ba-1710073781; shshshfpx=f9136121-78e7-0947-12fc-9805261422ba-1710073781; unpl=JF8EAJpnNSttXkpSVkkEGEYXTVVTWw4BHB9QbzJXAA1bSgcESwAcRhZ7XlVdWBRKEh9ubhRUWlNIUA4aBSsSEXteU11bD00VB2xXXAQDGhUQR09SWEBJJV1WWVsLTxQEbGINZG1bS2QFGjIbGxVKW1ZdXwBLJwJfYDVkbVtLVgQbBysTIEptFgoBAUkQA25uSFRUXUpSBxgAExIgSm1X; __jdv=76161171|haosou-search|t_262767352_haosousearch|cpc|13672526249_0_707bc72e67964b8f9b1dcea20b0a36e7|1712564708316; areaId=10; PCSYCityID=CN_230000_230100_0; mba_muid=1840732391; wlfstk_smdl=5pk1x2256h9o2kojbxmz7jolgrj84mra; TrackID=13q2TDE6V77Uk5at0TpoOdic7dicYtCetrDLAUBF64kn0peanu2zGDEiaYA1-GWN5sWRojfAlrb40fZzfzSOeScgf26EK0fyg0R8LmLU9ZphryDnO0oPXtcDuQ79WcgxZ; thor=803B995CB40894DFE2FBB64F13264FE9AA909FE05BC59B4DCF5ABBDB7534A455BF50123C1F0F43FD065235EA090280E42A73B248FA892B3CA9AC371F69B885FFA30FE520BDFB40EF0C6B66D9E6BC85BF2D427B1B721F32A4B900328B16D59191FF8B2E403088B85F27B435711151B666FD0CB99DE7C51B4661443AB821D06C6A88EC2F7588847A1DF5C4DF4CB55A74883E08F804C8AE094F7278309912010C25; flash=2_zwTXq9J04r9QRsvFM4l17MYOZzHOXtUQN7hnmLXtjbcRltPf0TMI1L_GxmCGAKl3MB-5lhj--0puOyaLIOe8cmIBzRgy61EUzvgStU_PhXN*; pinId=6eqGBBhqhSFL4lzuscJYrbV9-x-f3wj7; pin=jd_6417e9bce0665; unick=jd_6417e9bce0665; ceshi3.com=000; _tp=%2BRgoMk5G7WxI9a8KI8um3pPeYi3dPPoSI0Edd3I5rPQ%3D; _pst=jd_6417e9bce0665; 3AB9D23F7A4B3C9B=TDQZYIZYON5CRNYERGVK32SRCFCAHDSI62R5XAOKAHTQEH4JOQ6MBBFUV5UJVIZMY2KIDMJKLAVRLGG2GPPNNYYOQA; __jda=181111935.1840732391.1710073773.1710073774.1712564708.2; __jdc=181111935; ipLoc-djd=10-698-707-46023; 3AB9D23F7A4B3CSS=jdd03TDQZYIZYON5CRNYERGVK32SRCFCAHDSI62R5XAOKAHTQEH4JOQ6MBBFUV5UJVIZMY2KIDMJKLAVRLGG2GPPNNYYOQAAAAAMOXTR4PMQAAAAADTWZKBKQB7H6KIX; shshshfpb=BApXeHnDrv-tA5c8xiqDn86A18XKd0pNgBlJGMK5t9xJ1MiD3moO2',
                    'referer': 'https://search.jd.com/'
                }
                # 发生请求并获取json数据
                resp = requests.get(url, params=params, headers=headers).json()
                if not resp['comments']:
                    print(f'============================第{page + 1}页为空===============================')
                    return render(request, "spider_list.html", context)
                # 获取评论内容并保存
                for comment in resp['comments']:
                    # 将评论内容里的换行符剔除
                    content = comment['content'].replace('\n', '')
                    comment_time = comment['creationTime']
                    score = comment['score']
                    # print(score, comment_time, content)  # print并不能打印出所有的字符
                    csvwriter.writerow((score, comment_time, content))

                print(f'============================第{page + 1}页爬取完毕===============================')

                print("准备sleep")
                time.sleep(5 + random.random())
                print("正在爬取！")

            except:
                break

    global FLAG
    print("爬虫",FLAG)
    FLAG = 1
    return render(request, "spider_list.html", context)


def spider_download(request):
    print(os.getcwd())
    path = os.path.join(os.getcwd(), "spider_comment", "JD_comment.csv")

    f = open(path, "rb")
    print(path)
    print(f)
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="JD_comment.csv"'
    return response


def spider_wait(request):
    print(FLAG)
    if not FLAG:
        print("False",FLAG)
        return JsonResponse({'status': False})

    return JsonResponse({'status': True})