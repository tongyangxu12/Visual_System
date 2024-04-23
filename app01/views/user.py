from django.shortcuts import render, redirect
from django.http import JsonResponse
from app01 import models
from app01.utils.form import UserResetModelForm, UserEditModelForm


def user_list(request):
    obj = models.UserInfo.objects.filter(id = request.session['info'].get("id")).first()
    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")
    print(obj.username)
    if obj.username == "root":
        obj = models.UserInfo.objects.exclude(id = request.session['info'].get("id"))
        print(obj)
        return render(request, "admin_list.html", {"obj": obj, "img_path": img_path})

    return render(request, "user_list.html", {"obj": obj, "img_path": img_path})


def user_reset(request, nid):
    """重置用户密码"""
    # 对象 / None
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    img_path = models.UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = UserResetModelForm()
        return render(request, 'father_yemian.html', {'form': form, 'title': title, "img_path": img_path})

    form = UserResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'father_yemian.html', {'form': form, 'title': title})



def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    title = '编辑用户名'

    if request.method == 'GET':
        form = UserEditModelForm(instance=row_object)
        return render(request, 'father_yemian.html', {'form': form, 'title': title})

    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'father_yemian.html', {'form': form, 'title': title})


def user_delete(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
