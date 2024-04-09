from django.shortcuts import render, redirect
from app01.models import UserInfo
from app01.utils.form import UpModelForm
"""
更改头像 视图函数
"""


def avatar_edit(request):
    """更改头像"""

    img_path = UserInfo.objects.filter(id=request.session['info'].get("id")).values("img").first()
    img_path = img_path.get("img")

    if request.method == 'GET':
        return render(request, 'avatar_edit.html', {"img_path": img_path})

    file = request.FILES.get('avatar')
    file_name = 'avatar/' + file.name

    with open("media/"+file_name, 'wb+') as fo:
        for chunk in file.chunks():
            fo.write(chunk)

    print(file_name)
    UserInfo.objects.filter(id=request.session["info"].get("id")).update(img=file_name)

    return redirect('/user/list/')


    # info = request.session.get('info')
    # request.session['info'] = {
    #     'id': info['id'],
    #     'name': info['name'],
    #     'avatar': '/'+file_name,
    # }




