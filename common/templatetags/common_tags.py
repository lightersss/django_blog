from django import template
from django.utils.text import Truncator
register = template.Library()
#不需要在Installed app中进行注册！！！！
@register.filter(name='loop_ban')  # 过滤器在模板中使用时的name
def loop_ban(value):
    list=find_all('?from=',value)
    if list!=-1:
        if len(list)>=1:
            value=str(value)[list[-1]+6:]
    return value




def find_all(sub, s):
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index + 1)

    if len(index_list) > 0:
        return index_list
    else:
        return -1

