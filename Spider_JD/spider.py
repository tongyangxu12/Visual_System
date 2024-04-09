# 导入程序用到的包
import requests
import time
import random
import csv

# 获取评论
def get_content(page):
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
        'cookie':'__jdu=1840732391; shshshfpa=f9136121-78e7-0947-12fc-9805261422ba-1710073781; shshshfpx=f9136121-78e7-0947-12fc-9805261422ba-1710073781; unpl=JF8EAJpnNSttXkpSVkkEGEYXTVVTWw4BHB9QbzJXAA1bSgcESwAcRhZ7XlVdWBRKEh9ubhRUWlNIUA4aBSsSEXteU11bD00VB2xXXAQDGhUQR09SWEBJJV1WWVsLTxQEbGINZG1bS2QFGjIbGxVKW1ZdXwBLJwJfYDVkbVtLVgQbBysTIEptFgoBAUkQA25uSFRUXUpSBxgAExIgSm1X; __jdv=76161171|haosou-search|t_262767352_haosousearch|cpc|13672526249_0_707bc72e67964b8f9b1dcea20b0a36e7|1712564708316; areaId=10; PCSYCityID=CN_230000_230100_0; mba_muid=1840732391; wlfstk_smdl=5pk1x2256h9o2kojbxmz7jolgrj84mra; TrackID=13q2TDE6V77Uk5at0TpoOdic7dicYtCetrDLAUBF64kn0peanu2zGDEiaYA1-GWN5sWRojfAlrb40fZzfzSOeScgf26EK0fyg0R8LmLU9ZphryDnO0oPXtcDuQ79WcgxZ; thor=803B995CB40894DFE2FBB64F13264FE9AA909FE05BC59B4DCF5ABBDB7534A455BF50123C1F0F43FD065235EA090280E42A73B248FA892B3CA9AC371F69B885FFA30FE520BDFB40EF0C6B66D9E6BC85BF2D427B1B721F32A4B900328B16D59191FF8B2E403088B85F27B435711151B666FD0CB99DE7C51B4661443AB821D06C6A88EC2F7588847A1DF5C4DF4CB55A74883E08F804C8AE094F7278309912010C25; flash=2_zwTXq9J04r9QRsvFM4l17MYOZzHOXtUQN7hnmLXtjbcRltPf0TMI1L_GxmCGAKl3MB-5lhj--0puOyaLIOe8cmIBzRgy61EUzvgStU_PhXN*; pinId=6eqGBBhqhSFL4lzuscJYrbV9-x-f3wj7; pin=jd_6417e9bce0665; unick=jd_6417e9bce0665; ceshi3.com=000; _tp=%2BRgoMk5G7WxI9a8KI8um3pPeYi3dPPoSI0Edd3I5rPQ%3D; _pst=jd_6417e9bce0665; 3AB9D23F7A4B3C9B=TDQZYIZYON5CRNYERGVK32SRCFCAHDSI62R5XAOKAHTQEH4JOQ6MBBFUV5UJVIZMY2KIDMJKLAVRLGG2GPPNNYYOQA; __jda=181111935.1840732391.1710073773.1710073774.1712564708.2; __jdc=181111935; ipLoc-djd=10-698-707-46023; 3AB9D23F7A4B3CSS=jdd03TDQZYIZYON5CRNYERGVK32SRCFCAHDSI62R5XAOKAHTQEH4JOQ6MBBFUV5UJVIZMY2KIDMJKLAVRLGG2GPPNNYYOQAAAAAMOXTR4PMQAAAAADTWZKBKQB7H6KIX; shshshfpb=BApXeHnDrv-tA5c8xiqDn86A18XKd0pNgBlJGMK5t9xJ1MiD3moO2',
        'referer': 'https://search.jd.com/'
    }
    # 发生请求并获取json数据
    resp = requests.get(url,params=params,headers=headers).json()
    # 获取评论内容并保存
    for comment in resp['comments']:
        # 将评论内容里的换行符剔除
        content = comment['content'].replace('\n','')
        comment_time = comment['creationTime']
        score = comment['score']
        print(score, comment_time, content)
        csvwriter.writerow((score, comment_time, content))
    print(f'============================第{page+1}页爬取完毕===============================')

if __name__ == '__main__':
    product_id = input('请输入商品的ID：')
    page_number = int(input('请输入要爬取的页数：'))
    with open(f'./comments/JD_comment_{product_id}.csv','a',encoding='utf_8_sig')as f:

        csvwriter = csv.writer(f)
        csvwriter.writerow(('评分', '评论时间', '评论内容'))

        for page in range(page_number):
            try:
                get_content(page)
                time.sleep(5+random.random())
            except:
                break
    print(f'爬虫已完成！爬取到的内容请在comments目录下的 JD_comment_{product_id}.csv 查看！')
    print("hello")
