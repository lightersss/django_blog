from django import template
from comment.models import CommentRecord
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount,LikeRecord
register = template.Library()

@register.simple_tag
def get_like_count(obj):
    contenttype = ContentType.objects.get_for_model(obj)
    count,created = LikeCount.objects.get_or_create(content_type=contenttype, object_id=obj.id)
    return count.like_count

@register.simple_tag(takes_context=True)
def get_like_status(context,obj):
    user=context['user']
    contenttype = ContentType.objects.get_for_model(obj)
    if user.is_authenticated:
        if LikeRecord.objects.filter(content_type=contenttype, object_id=obj.id,like_user=user).exists():
            return 'active-thumbs-up'
        else:
            return ''
    else:
        return ''

@register.simple_tag()
def get_contenttype(obj):
    contenttype=ContentType.objects.get_for_model(obj)
    return contenttype.model