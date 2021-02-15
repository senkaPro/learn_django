from django.urls import path
from .views import AddNewBlog, EditBlog,AddNewBlogPost

urlpatterns = [
    path('blog/new/', AddNewBlog.as_view(), name='new-blog'),
    path('blog/<int:pk>/update/', EditBlog.as_view(), name='edit-blog'),
    path('blogpost/add/', AddNewBlogPost.as_view(), name='new-blogpost'),
    path('blogpost/<int:pk>/update/', AddNewBlogPost.as_view(), name='blogpost-edit'),

]
