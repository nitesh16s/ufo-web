import json
import re
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from apps.blogs.models import(
    Blog,
    Comment,
    SaveBlog,
    LikeBlog,
    Activity
)
from apps.blogs.forms import CommentForm
from apps.users.models import Follow, Profile
from django.core import serializers
from django.contrib.auth.decorators import login_required


def category_blogs(request, slug):
    '''
    Function for fetching blogs based on activity.
    '''
    activity = get_object_or_404(Activity, slug=slug)
    blogs = Blog.objects.select_related().filter(activity=activity.id)
    context = {
        'blogs': blogs,
        'activities': Activity.objects.values(
            'activity', 'slug').order_by('-id')
    }
    return render(request, 'blogs/category.html', context)


def blog_search(request):
    query = request.GET['q']
    blogs = Blog.objects.select_related().filter(title__icontains=query)
    activities = Activity.objects.values(
        'activity', 'slug').order_by('-id')
    context = {
        'blogs': blogs,
        'activities': activities
    }
    return render(request, 'blogs/blog_search_results.html', context)


class BlogListView(View):
    '''
    View for listing all the blogs.
    '''

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects\
            .prefetch_related('activity')\
            .select_related().all()
        activities = Activity.objects.values(
            'activity', 'slug').order_by('-id')
        context = {
            'blogs': blogs,
            'activities': activities,
        }
        return render(request, 'blogs/blogs.html', context)


class BlogCreateView(LoginRequiredMixin, CreateView):
    '''
    View for adding new blogs.
    '''

    model = Blog
    fields = [
        'seo',
        'tags',
        'title',
        'blog_image',
        'content',
        'package',
        'activity',
        'continent',
        'country',
        'region']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogDetailView(View):
    '''
    View for details of a blog.
    '''

    def get(self, request, slug, *args, **kwargs):
        # Get the blog
        blog = get_object_or_404(Blog.objects.select_related(), slug=slug)
        # Get the comments, join to the comment author profile
        comments = blog.comments.select_related('author__profile')
        # Get the total likes
        total_likes = LikeBlog.objects.filter(blog=blog, is_liked=True).count()
        # Get the activities
        activities = Activity.objects.values(
            'activity', 'slug').order_by('-id')

        saved, liked, followed = None, None, None
        # when user is authenticated
        if request.user.is_authenticated:
            # check bookmarked by user or not.
            try:
                saved = SaveBlog.objects.get(
                    user=request.user, blog=blog, is_saved=True)
            except SaveBlog.DoesNotExist:
                saved = False
        # check user liked this or not.
            try:
                liked = LikeBlog.objects.get(
                    user=request.user, blog=blog, is_liked=True)
            except LikeBlog.DoesNotExist:
                liked = False

            # check user following the author or not.
            try:
                followed = Follow.objects.get(
                    from_user=request.user, to_user=blog.author, is_follow=True)
            except Follow.DoesNotExist:
                followed = False

        # pass all the data to the template.
        context = {
            'blog': blog,
            'comments': comments,
            'comment_form': CommentForm(),
            'saved': saved,
            'liked': liked,
            'followed': followed,
            'total_likes': total_likes,
            'activities': activities,
        }
        return render(request, 'blogs/blog_detail.html', context)


class CommentListView(LoginRequiredMixin, View):
    '''
    View for fetching all comments of a blog. Not using it.
    '''

    def get(self, request, pk, *args, **kwargs):
        blog = get_object_or_404(Blog, id=pk)
        comments = blog.comments.all()
        comments = serializers.serialize(
            'json', blog.comments.all().order_by('-id'))
        comments = json.loads(comments)
        return JsonResponse(comments, safe=False)
        # return HttpResponse(comments, content_type='application/json')


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''
    View for adding comments. 
    '''

    def get(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        return redirect('blog_detail', slug=blog.slug)

    def post(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        author = request.user
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            Comment.objects.create(blog=blog, author=author, content=content)
            messages.success(request, 'Comment created successfully.')
            return redirect('blog_detail', slug=blog.slug)
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('blog_detail', slug=blog.slug)


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    '''
    View for adding new blogs.
    '''

    model = Comment
    fields = ['content']
    template_name = 'blogs/update_comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def saveblog(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    user = request.user
    try:
        saved = SaveBlog.objects.get(blog=blog, user=user)
        if saved.is_saved == True:
            saved.is_saved = False
            saved.save()
            data = {
                'success': True,
                'msg': 'Unsaved'
            }
            return JsonResponse(data)
        else:
            saved.is_saved = True
            saved.save()
            data = {
                'success': True,
                'msg': 'Saved'
            }
            return JsonResponse(data)
    except SaveBlog.DoesNotExist:
        SaveBlog.objects.create(blog=blog, user=request.user, is_saved=True)
        data = {
            'success': True,
            'msg': 'Saved'
        }
        return JsonResponse(data)


@login_required
def likeblog(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    user = request.user
    try:
        liked = LikeBlog.objects.get(blog=blog, user=user)
        if liked.is_liked == True:
            liked.is_liked = False
            liked.save()
            total_likes = blog.likes.filter(is_liked=True).count()
            data = {
                'success': True,
                'msg': 'Disliked',
                'total_likes': total_likes
            }
            return JsonResponse(data)
        else:
            liked.is_liked = True
            liked.save()
            total_likes = blog.likes.filter(is_liked=True).count()
            data = {
                'success': True,
                'msg': 'Liked',
                'total_likes': total_likes
            }
            return JsonResponse(data)
    except LikeBlog.DoesNotExist:
        LikeBlog.objects.create(blog=blog, user=request.user, is_liked=True)
        total_likes = blog.likes.filter(is_liked=True).count()
        data = {
            'success': True,
            'msg': 'Liked',
            'total_likes': total_likes
        }
        return JsonResponse(data)


@login_required
def replies(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replies = comment.replies.all()
    if len(replies) == 0:
        data = {
            'replies': 0
        }
        return JsonResponse(data)
    else:
        profiles = []
        # bad code
        for reply in replies:
            profile = Profile.objects.get(id=reply.author.id)
            profiles.append(profile)
        replies = serializers.serialize('json', replies)
        profiles = serializers.serialize('json', profiles)
        replies = json.loads(replies)
        profiles = json.loads(profiles)
        data = {
            'content': replies[0]['fields']['content'],
            'createdAt': replies[0]['fields']['createdAt'],
            'profile_picture': profiles[0]['fields']['profile_picture'],
            'username': profiles[0]['fields']['slug'],
        }
        return JsonResponse(data, safe=False)
