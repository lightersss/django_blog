from django.db import models
from django.contrib.contenttypes.models import ContentType
from common.models import MyUser
from read_statistics.models import ReadCountExpand
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class BlogType(models.Model):
    type_name=models.CharField(max_length=50,verbose_name='博客类型名称')

    def __str__(self):
        return self.type_name

    class Meta:
        db_table='blogType'


class Blog(models.Model,ReadCountExpand):
    title=models.CharField(max_length=50,verbose_name='博客标题')
    blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE,verbose_name='博客类型')
    content=RichTextUploadingField(verbose_name='博客内容')
    author=models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_updated_time=models.DateTimeField(auto_now=True,verbose_name='最后更新时间')
    #read_count=models.PositiveIntegerField(default=0,verbose_name='阅读量')

    def __str__(self):
        return '标题:{0}  作者:{1}'.format(self.title,self.author.username)

    def get_email(self):
        return self.author.email

    def get_url(self):
        return reverse('blog:get_blog_detail',kwargs={'blog_id':self.id})





    class Meta:
        db_table='blog'
        ordering=['-created_time']





