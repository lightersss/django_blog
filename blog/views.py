from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractYear

from read_statistics.utils import read_count_plus_one
from .models import Blog,BlogType
from common.forms import LoginForm
from comment.models import CommentRecord

def get_all_blog_list(request):
    context={}
    raw_blogs=Blog.objects.all()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(raw_blogs, 5)#分页器 包含属性：分了多少页 一共多少个东西被分页了 页码范围
    page_of_blogs = paginator.get_page(page_num)#页 包含属性：object_list 是否有前后页 当前页页码
    #

    blogTypes, blog_created_date = common_context()

    context['page_of_blogs']=page_of_blogs
    context['paginator'] = paginator

    context['blogTypes'] = blogTypes
    context['blog_created_date']=blog_created_date
    return render(request,'get_blog_list.html',context)

def get_blog_detail_by_id(request,blog_id):
    context={}
    blog=get_object_or_404(Blog,id=blog_id)
    key=read_count_plus_one(request,blog)

    pre_blog=Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    blogTypes, blog_created_date = common_context()
    Blog_Class=ContentType.objects.get_for_model(blog)
    # comments=CommentRecord.objects.filter(content_type=Blog_Class,object_id=blog_id,parent=None)#root=None
    #博客相关内容
    context['blog']=blog
    #上下篇
    context['next_blog']= next_blog
    context['pre_blog'] = pre_blog
    #右侧栏内容
    context['blogTypes'] = blogTypes
    context['blog_created_date'] = blog_created_date
    #评论表单 转移到comment-tag中了
    # comment_form=CommentForm(initial={'contenttype':'blog','object_id':blog.id,'comment_be_replied_id':'0'})
    # context['form']=comment_form
    #评论内容
    # context['comments']=comments.order_by('-comment_time')
    context['comment_count']=CommentRecord.objects.filter(content_type=Blog_Class,object_id=blog.id).count()

    #模态框登陆表单
    context['form']=LoginForm()
    response=render(request,'get_blog_detail.html', context)
    response.set_cookie(key,'true')
    return response

def get_blog_list_by_type(request,blog_type_id):
    context={}
    blogType=get_object_or_404(BlogType,id=blog_type_id)
    raw_blogs=Blog.objects.filter(blog_type__id=blog_type_id)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(raw_blogs, 5)
    page_of_blogs = paginator.get_page(page_num)
    #分页器
    context['page_of_blogs'] = page_of_blogs
    context['paginator'] = paginator

    #右侧栏
    context['blogType']=blogType
    blogTypes, blog_created_date = common_context()
    context['blogTypes'] = blogTypes
    context['blog_created_date'] = blog_created_date
    return render(request,'get_blog_list_by_type.html',context)


def get_blog_list_by_year_month(request,year,month):
    context={}
    raw_blogs=Blog.objects.filter(created_time__year=year,created_time__month=month)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(raw_blogs, 5)
    page_of_blogs = paginator.get_page(page_num)
    context['page_of_blogs'] = page_of_blogs
    context['paginator'] = paginator
    blogTypes, blog_created_date = common_context()
    context['blogTypes'] = blogTypes
    context['blog_created_date'] = blog_created_date
    return render(request,'get_blog_list_by_year_month.html',context)


def common_context():
    blog_created_date = Blog.objects \
        .annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time')) \
        .values('year', 'month').order_by('year', 'month').annotate(count=Count('created_time'))
    blogTypes = BlogType.objects.annotate(blog_count=Count('blog'))
    return blogTypes,blog_created_date