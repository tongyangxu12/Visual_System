from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect,HttpResponse
class AuthMiddleware(MiddlewareMixin):
    """ 登录检查中间件 """

    def process_request(self,request):

        # 0.排除那些不需要校验就能访问的页面
        # path_info获取当前的url信息
        url = request.path_info
        # 如果当前访问的url是登录页面及图片验证里面的图片就直接放行,return None
        if url in ["/login/", "/image/code/", "/register/"]:
            return None

        # 1.读取当前访问用户的session信息,用session.get("xxxx")
        info_dict = request.session.get("info")
        # 如果登录过,返回None
        if info_dict:
            # print("pass")
            return None
        # 如果没有登陆过,返回到登陆页面
        else:
            # print("no")
            # print("auth", request.session)
            return redirect('/login/')

    # 这个process_response对于登录完全没有用
    def process_response(self, request, response):
        # print("M1走了")
        return response