from django.contrib import admin
from apps.blogs.models import Blog, Comment, Reply, SaveBlog

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(SaveBlog)
