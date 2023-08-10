from django.urls import path
from apps.blogs.views import (
    BlogListView,
    BlogCreateView,
    BlogDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentListView,
    category_blogs,
    saveblog,
    likeblog,
    replies,
    blog_search
)

urlpatterns = [
    path('blogs', BlogListView.as_view(), name='blogs'),
    path('new/blog', BlogCreateView.as_view(), name='create_blog'),
    path('blog/<str:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/category/<str:slug>', category_blogs, name='blog_category'),
    path('blog/<str:slug>/new/comment',
         CommentCreateView.as_view(), name='create_comment'),
    path('blog/comment/<str:slug>/update', CommentUpdateView.as_view(), name='update_comment'),
    path('blog/<int:pk>/comments',
         CommentListView.as_view(), name='show_comments'),
    path('blog/<int:pk>/save', saveblog, name='save_blog'),
    path('blog/<int:pk>/like', likeblog, name='like_blog'),
    path('blog/search', blog_search, name='blog_search'),
    path('blog/comment/<int:pk>/replies', replies, name='replies')
]
