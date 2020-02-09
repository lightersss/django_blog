from django.contrib import admin
from .models import CommentRecord
# Register your models here.
@admin.register(CommentRecord)
class CommentRecordAdmin(admin.ModelAdmin):
    list_display=('id','content_object','comment_content','comment_time','comment_user')