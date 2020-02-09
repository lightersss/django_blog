from django.contrib import admin
from .models import MyUser,BlogType,Blog#,ReadRecord
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','get_read_num','blog_type','content','author','created_time','last_updated_time')

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')


# @admin.register(ReadRecord)
# class ReadRecordAdmin(admin.ModelAdmin):
#     list_display = ('id', 'read_count','blog')
