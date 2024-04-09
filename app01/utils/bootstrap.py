from django import forms
"""
定义完这个类后，视图函数里面ModelForm可以继承这个类然后把__init__()给删了
其他的什么钩子函数不用管，只要哪个ModelForm想有bootstrap样式就继承BootStrapModelForm
"""
class BootStrapModelForm(forms.ModelForm):
    # 把不希望添加样式的字段写到这里面,后面在for循环添加样式的时候可以加个if判断
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                # 如果name在不想添加样式的列表中,就continue跳过
                continue

            # 字段中有属性的，保留原来的属性；没有属性的，才增加属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
                field.widget.attrs["style"] = "margin-bottom: 5px"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                    "style": "margin-bottom: 5px"
                }


class BootStrapForm(forms.Form):
    # 把不希望添加样式的字段写到这里面,后面在for循环添加样式的时候可以加个if判断
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                # 如果name在不想添加样式的列表中,就continue跳过
                continue

            # 字段中有属性的，保留原来的属性；没有属性的，才增加属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
                field.widget.attrs["style"] = "margin-bottom: 5px"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                    "style": "margin-bottom: 5px"
                }