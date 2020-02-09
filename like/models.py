from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import MyUser
# Create your models here.
class LikeRecord(models.Model):
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    like_time=models.DateTimeField(auto_now_add=True)
    like_user=models.ForeignKey(MyUser,on_delete=models.CASCADE)

class LikeCount(models.Model):
    like_count=models.PositiveIntegerField(default=0,verbose_name='点赞数')
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')