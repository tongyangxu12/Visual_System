## Visual_System 毕业设计

#### 1.项目介绍

本项目为“服装产品消费评论挖掘与可视化”毕设的可视化部分，基于Django进行开发、echarts进行绘图

#### 2.项目功能

（1）用户管理：在本项目中，用户可以进行注册、登录，未登录的用户只能访问register、login页面，用户还可以重置密码、更换头像

（2）爬虫：在本项目中，用户可以输入要爬取的商品编号（以某东为例）、爬取页数来获取商品的评论数据，爬取完成后生成的CSV可以下载到本地

（3）上传商品评论数据：在本项目中，用户可以上传商品评论数据，上传的数据包括：数据报告名称、详细信息、所属用户和上传的CSV文件

（4）处理数据并进行可视化：在本项目中，用户可以对上传的数据进行处理和可视化展示，有情感分析、聚类分析和LDA主题分析三个部分

#### 3.目录结构

```
Visual_System
├── app01
	├── middleware
	├── migrations
	├── static
	├── templates
	├── utils
	├── views
	├── __init__.py
	├── admin.py
	├── apps.py
	├── models.py
	├── tests.py
├── Cluster_Analysis
	├── cluster_analysis.py
	├── JD_comment.csv
	├── 停用词库.txt
├── LDA_Analysis
	├── JD_comment.csv
	├── lda_analysis.py
	├── 停用词库.txt
├── media
	├── avatar
	├── data
├── Sentiment_Analysis
	├── JD_comment.csv
	├── sentiment_analysis.py
	├── 停用词库.txt
├── spider_comment
	├── JD_comment.csv
├── Spider_JD
	├── comments
	├── spider.py
├── Visual_System
	├── __init__.py
	├── asgi.py
	├── settings.py
	├── urls.py
	├── wsgi.py
├── manage.py
├── Monaco.ttf
├── requirements.txt
├── 停用词库.txt
```

#### 4.安装说明

```
1. 配置Python解释器
	项目的版本：Python3.11.3
    windows版python3.11.3下载链接: 
        https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
    注意，安装时，一定要勾选add python to path!!!!!
    或者使用anaconda新建虚拟环境
    conda create -n visual_system python=3.11.3
    
    然后在pycharm上配置python解释器

2. 更新pip
    打开控制台，执行
        pip install --upgrade pip

3. 安装依赖包
    进入项目处，打开控制台，执行 
        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    命令，等待下载安装完毕

4. 启动网页服务器
    进入项目处，打开控制台，执行
        python manage.py runserver
    然后浏览器打开链接即可
        http://127.0.0.1:8000/
```



#### 5.使用说明

```
# 第二次运行
启动网页服务器
    进入项目处，打开控制台，执行
        python manage.py runserver
    然后浏览器打开链接即可
        http://127.0.0.1:8000/
```

