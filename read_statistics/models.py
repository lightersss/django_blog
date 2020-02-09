from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class ReadRecord(models.Model):
    read_count=models.PositiveIntegerField(default=0,verbose_name='阅读量')
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    def __str__(self):
        return str(self.read_count)

class ReadCountExpand():
    def get_read_num(self):
        try:
            contenttype = ContentType.objects.get_for_model(self)
            readnum=ReadRecord.objects.get(content_type=contenttype,object_id=self.id)
            return readnum
        except exceptions.ObjectDoesNotExist:
            return 0