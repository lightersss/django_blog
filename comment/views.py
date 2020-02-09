from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import CommentRecord
from .forms import CommentForm

from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def submit_comment(request):
    # if request.user.is_authenticated:
    # 已登录
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    commentForm = CommentForm(request.POST, user=request.user)
    if commentForm.is_valid():
        parent = commentForm.cleaned_data['parent']
        content_object = commentForm.cleaned_data['content_object']
        comment_content = commentForm.cleaned_data['comment_content']
        if parent is None:  # 直接评论
            comment = CommentRecord.objects.create(content_object=content_object, comment_content=comment_content,
                                                   comment_user=request.user)
            comment.send_email()





        else:  # 回复评论
            comment = CommentRecord.objects.create(content_object=content_object, comment_content=comment_content,
                                                   comment_user=request.user, parent=parent,
                                                   user_replied=parent.comment_user,
                                                   root=parent.root if parent.root else parent)
            comment.send_email()

        data = {}
        data['status'] = 'success'
        data['username'] = comment.comment_user.username
        data['time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M')
        data['text'] = comment.comment_content
        data['content_type']=ContentType.objects.get_for_model(comment).model
        if parent is None:
            data['user_replied']=''
        else:
            data['user_replied']=comment.user_replied.username
        data['pk']=comment.pk
        data['root_pk'] = comment.root.pk if comment.root else ''
        return JsonResponse(data)
    else:
        data = {}
        data['status'] = 'error'
        data['message'] = list(commentForm.errors.values())[0]
        return JsonResponse(data)
# else:
#     #未登录
#     return render(request,'error.html',{'message':'先登录'})
