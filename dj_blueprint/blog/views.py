from django.forms import fields
from django.db.models import Exists
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls.base import reverse
from django.http import HttpResponseRedirect,HttpResponseForbidden, request
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django import forms
from django.views import generic

from .models import Blog, BlogPost
from django.views.generic import CreateView,TemplateView, UpdateView, ListView


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if Blog.objects.filter(owner= self.request.user).exists():
                context["has_blog"] = True
                blog = Blog.objects.get(owner=self.request.user)
                context['blog'] = blog
                context['blogpost'] = BlogPost.objects.filter(blog=blog).all()
        return context


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title',]

class AddNewBlog(CreateView):
    form_class = BlogForm
    template_name = 'blog_settings.html'

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.owner = self.request.user
        blog.slug = slugify(blog.title)
        blog.save()
        return HttpResponseRedirect('/')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if Blog.objects.filter(owner=request.user).exists():
            return HttpResponseForbidden('You cannot add more than one blog')
        else:
            return super(AddNewBlog, self).dispatch(request, *args, **kwargs)





class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body',]

class AddNewBlogPost(CreateView):
    form_class = BlogPostForm
    template_name = 'blogpost.html'
    success_url = 'home'

    def form_valid(self, form):
        blogpost = form.save(commit=False)
        blogpost.blog = Blog.objects.get(owner=self.request.user)
        blogpost.slug = slugify(blogpost.title)
        blogpost.is_published = True
        blogpost.save()
        return HttpResponseRedirect(reverse('home'))

    def dispatch(self, request, *args, **kwargs):
        return super(AddNewBlogPost, self).dispatch(request, *args, **kwargs)
    

class EditBlogPost(UpdateView):
    template_name = 'blogpost_list.html'
    model = BlogPost
    form_class = BlogPostForm
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBlogPost, self).dispatch(request, *args, **kwargs)

class BlogPostList(ListView):
    template_name = 'blogpost_list.html'
    context_object_name = BlogPost
    queryset = BlogPost.objects.all()



class EditBlog(UpdateView):
    form_class = BlogForm
    template_name = 'blog_edit.html'
    model = Blog
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBlog, self).dispatch(request, *args, **kwargs)

class BlogListView(ListView):
    template_name = 'bloglist.html'
    model = Blog

    def get_queryset(self, request):
        q = super(BlogListView, self).get_queryset(request, *args, **kwargs)
        return q.filter(blog__owner=self.request.user)
    