from django.db import models


class UserInfo(models.Model):
    """ 用户信息表 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    img = models.FileField(verbose_name='Logo', max_length=128, upload_to='avatar/', default="/avatar/init.jpg")

    def __str__(self):
        return self.username


class Order(models.Model):
    """商品信息表"""
    oid = models.CharField(verbose_name="商品编号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)

    admin = models.ForeignKey(verbose_name="所属用户", to="UserInfo", on_delete=models.CASCADE)


class CsvData(models.Model):
    """ csv数据表 """
    title = models.CharField(verbose_name='数据表格名称', max_length=32)
    detail = models.TextField(verbose_name='详细信息')
    admin = models.ForeignKey(verbose_name="所属用户", to="UserInfo", on_delete=models.CASCADE)

    data = models.FileField(verbose_name="上传的数据", max_length=128, upload_to='data/')