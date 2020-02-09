from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import MyUser
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string
class SendEmail(threading.Thread):
    def __init__(self,subject,text,email,fail_silently=False):
        self.subject=subject
        self.text=text
        self.email=email
        self.fail_silently=fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail('新的通知', '', 'gh632830515@126.com', [self.email], fail_silently=False,html_message=self.text)

class CommentRecord(models.Model):
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_content=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    comment_user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='comments')

    #回复评论
    parent=models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name='parent_comment')
    user_replied=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,related_name='replys')
    root=models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name='root_comment')
    class Meta:
        ordering=['comment_time']

    def send_email(self):
        if self.parent is None:
            text = self.comment_content + '\n' + '<a href="'+self.content_object.get_url()+'">点击查看</a>'
            #text=render_to_string('XXXX.html',{'a':1,'b':2})
            # text=render(None,'XXXX.html',{'a':1,'b':2}).content.decode('utf-8')
            email = self.content_object.get_email()
            send_mail=SendEmail(subject='新的评论',text=text,email=email)
            send_mail.start()
        else:
            text = self.comment_content + '\n' + '<a href="'+self.content_object.get_url()+'">点击查看</a>'
            email = self.content_object.get_email()
            send_mail = SendEmail(subject='新的回复', text=text, email=email)
            send_mail.start()