from django.contrib.contenttypes.models import ContentType


from read_statistics.models import ReadRecord
def read_count_plus_one(request,object):
    contenttype = ContentType.objects.get_for_model(object)#get_for_model参数可以为类或者类的实例
    key="%s_%s_read"%(contenttype.model,object.id)
    if not request.COOKIES.get(key):

        if ReadRecord.objects.filter(content_type=contenttype, object_id=object.id).count():
            readrecord = ReadRecord.objects.get(content_type=contenttype, object_id=object.id)
            readrecord.read_count += 1
            readrecord.save()
        else:
            readrecord = ReadRecord(content_type=contenttype, object_id=object.id)
            readrecord.read_count += 1
            readrecord.save()
    return key