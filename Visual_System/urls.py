"""
URL configuration for Visual_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from app01.views import user, account, order, analysis, avatar, sentiment_list, cluster_list, lda_list, spider_list, test

urlpatterns = [
    # path("admin/", admin.site.urls),

    # 默认访问用户列表页面
    path('', user.user_list),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 用户管理
    path("user/list/", user.user_list),
    path('user/<int:nid>/reset/', user.user_reset),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 头像
    path('avatar/edit/', avatar.avatar_edit),

    # 登录功能实现
    path("login/", account.login),
    # 注销,即退出登录功能
    path("logout/", account.logout),
    # 登录的时候添加图片验证
    path("image/code/", account.image_code),
    # 注册
    path('register/', account.register),

    # 商品管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 分析
    path('analysis/<int:nid>/sentiment/', analysis.analysis_sentiment),
    path('analysis/<int:nid>/cluster/', analysis.analysis_cluster),
    path('analysis/<int:nid>/lda', analysis.analysis_lda),

    # 情感分析
    path("sentiment/list/", sentiment_list.sentiment_list),  # sentiment_list同时包含了展示和添加两个功能
    path('sentiment/<int:nid>/delete/', sentiment_list.sentiment_delete),
    path('sentiment/<int:nid>/analysis/', sentiment_list.sentiment_analysis),
    path("sentiment/chart/one/", sentiment_list.chart_one),
    path("sentiment/chart/two/", sentiment_list.chart_two),
    path("sentiment/chart/three/", sentiment_list.chart_three),
    path("sentiment/chart/four/", sentiment_list.chart_four),

    # 聚类分析
    path("cluster/list/", cluster_list.cluster_list),  # sentiment_list同时包含了展示和添加两个功能
    path('cluster/<int:nid>/delete/', cluster_list.cluster_delete),
    path('cluster/<int:nid>/analysis/', cluster_list.cluster_analysis),
    path("cluster/chart/one/", cluster_list.chart_one),
    path("cluster/chart/two/", cluster_list.chart_two),
    path("cluster/chart/three/", cluster_list.chart_three),
    path("cluster/chart/four/", cluster_list.chart_four),

    # LDA分析
    path("lda/list/", lda_list.lda_list),
    path('lda/<int:nid>/delete/', lda_list.lda_delete),
    path('lda/<int:nid>/analysis/', lda_list.lda_analysis),
    path("lda/chart/one/", lda_list.chart_one),

    # 爬虫
    path("spider/list/", spider_list.spider_list),
    path("spider/download/", spider_list.spider_download),
    path("spider/wait/", spider_list.spider_wait),

    path("test/list/", test.test_list)


]
