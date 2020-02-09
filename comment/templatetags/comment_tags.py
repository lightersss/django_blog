from django import template
from comment.models import CommentRecord
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    contenttype=ContentType.objects.get_for_model(obj)
    count=CommentRecord.objects.filter(content_type=contenttype,object_id=obj.id).count()
    return count

@register.simple_tag
def get_comment_form(obj):
    contenttype = ContentType.objects.get_for_model(obj).model
    comment_form = CommentForm(initial={'contenttype': contenttype, 'object_id': obj.id, 'comment_be_replied_id': '0'})
    return comment_form

@register.simple_tag
def get_comment_list(obj):
    Blog_Class = ContentType.objects.get_for_model(obj)
    comments = CommentRecord.objects.filter(content_type=Blog_Class, object_id=obj.id, parent=None)  # root=None
    comments=comments.order_by('-comment_time')
    return comments