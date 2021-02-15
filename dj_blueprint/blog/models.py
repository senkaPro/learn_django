from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    owner = models.ForeignKey(User,editable=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=500,blank=False)
    slug = models.CharField(max_length=500, editable=False)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=500, blank=False)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    slug = models.SlugField( max_length=500 , unique=True)

    def __str__(self):
        return self.title
    