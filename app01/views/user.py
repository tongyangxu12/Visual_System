from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserResetModelForm


def user_list(request):
    obj = models.UserInfo.objects.filter(id = request.session['info'].get("id")).first()
    img_path = models.UserInfo.objects.filter(id = request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")
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
