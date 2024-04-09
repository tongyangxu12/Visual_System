from django.conf import settings
import hashlib
def md5(data_string):
    # 如果用md5加密，特定明文对应的密文是固定的，可以用加盐增加安全性
    # salt = "xxxxxx"

    # django在settings.py里给我们提供了SECRET_KEY进行加盐

    # 先实例化md5加密对象,加盐salt了
    # obj = hashlib.md5(salt.encode('utf-8'))
    # 利用SECRET_KEY加盐,SECRET_KEY是django自动随机生成的
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))

    # 对要加密的data_string进行加密
    obj.update(data_string.encode('utf-8'))
    # 返回密文
    return obj.hexdigest()