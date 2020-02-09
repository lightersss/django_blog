from django import template
from django.utils.text import Truncator
register = template.Library()
#注意在Installed app中进行注册！！！！
@register.filter(name='My_truncatechars')  # 过滤器在模板中使用时的name
def My_truncatechars(value, arg):  # 把传递过来的参数arg替换为'~'
    try:
        length = int(arg)
    except ValueError:  # Invalid literal for int().
        return value  # Fail silently.
    return Truncator(value).chars(length)+'...'
