from django import forms
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from .models import CommentRecord
class CommentForm(forms.Form):
    contenttype = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    comment_content = forms.CharField(widget=CKEditorWidget(config_name='comment_ck_conf'),
                                      error_messages={'required':'评论不能为空'})
    comment_be_replied_id=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'comment_be_replied_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user=kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_comment_be_replied_id(self):
        comment_be_replied_id=self.cleaned_data['comment_be_replied_id']
        if comment_be_replied_id<0:
            raise forms.ValidationError('回复出错')
        elif comment_be_replied_id==0:
            self.cleaned_data['parent']=None
        elif CommentRecord.objects.filter(id=comment_be_replied_id).exists():
            self.cleaned_data['parent']=CommentRecord.objects.get(id=comment_be_replied_id)
        else:
            raise forms.ValidationError('出错了')
        return comment_be_replied_id

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('尚未登陆')
        contenttype = self.cleaned_data['contenttype']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=contenttype).model_class()
            content_object = model_class.objects.get(id=object_id)
            self.cleaned_data['content_object'] = content_object
        except Exception as e:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data
