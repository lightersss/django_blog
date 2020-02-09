from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount,LikeRecord
# Create your views here.
def json_like_count(like_count):
    data={}
    data['status']='SUCCESS'
    data['like_count']=like_count
    return JsonResponse(data)

def json_error(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message']=message
    return JsonResponse(data)

def like_change(request):
    content_type=request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    is_like = request.GET.get('is_like')

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(id=object_id)
    except ObjectDoesNotExist:
        return json_error(401,'不存在')

    if not request.user.is_authenticated:

        return json_error(400, '未登录')
    if is_like=='true':#点赞

        likerecord,created=LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,like_user=request.user)
        if created:#新建记录
            likecount, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            likecount.like_count+=1
            likecount.save()
            return json_like_count(likecount.like_count)
        else:#已有记录。说明赞过
            return json_error(402,'已经点赞过')
    else:#取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, like_user=request.user):#已有记录，删掉记录，数量减一
            LikeRecord.objects.get(content_type=content_type, object_id=object_id, like_user=request.user).delete()
            likecount, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                likecount.like_count-=1
                likecount.save()
                return json_like_count(likecount.like_count)
            else:
                return json_error(404,'出错了')
        else:
            return json_error(403,'没赞过')
