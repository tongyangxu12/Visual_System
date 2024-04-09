"""
管理员 登录 注册 视图
"""

from django.shortcuts import render, redirect, HttpResponse
from app01.utils.form import LoginForm, AdminModelForm
from app01 import models
from app01.utils.code import check_code
from io import BytesIO


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象 / None
        admin_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}

        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/user/list/')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """
    # 这个url是显示图片的,也应该是不用登录就能访问,需要在中间件里面把/image/code/也加入白名单

    # 调用check_coke()方法,即pillow函数,生成图片
    # img是图片对象,code_string是写在图片上的验证码,要把img返回到urls.py里与视图函数image_code相对应的url网页中
    img, code_string = check_code()
    # 把图片上的验证码打印出来看看
    # print(code_string)

    # 把图片上的验证码写入到自己的session中,以便于后续获取验证码再进行校验
    request.session["image_code"] = code_string

    # 图片验证码不可能一直有效的,在设定的时间内可以用,过了就无效了
    request.session.set_expiry(60)

    # 此处我们不再像以前写到本地,因为存到本地返回的时候还要再读取,麻烦了
    # 而是用内存文件BytesIO,将img写到内存文件中,然后再从内存文件对象中取出图片
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


def register(request):
    """注册（添加用户）"""

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'register.html', {'form': form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})

