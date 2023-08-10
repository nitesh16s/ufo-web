import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.users.models import Profile, Follow
from apps.users.forms import UserNameForm
from apps.packages.models import (
    Bookings,
    OnRequestBookings,
    Review,
    Activity
)
from apps.blogs.models import Blog, SaveBlog
from apps.main.models import Query, Answer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core import serializers
from allauth.account.admin import EmailAddress


def email_verified_check(request):
    user = request.user
    is_verified = EmailAddress.objects.filter(
        user=user, verified=True).exists()
    return is_verified


@login_required
def profile(request):
    profile = request.user.profile
    age = profile.get_age()
    blogs = Blog.objects.select_related().filter(
        author=request.user).order_by('-id')
    saved = SaveBlog.objects.filter(is_saved=True, user=request.user)
    queries = Query.objects.filter(
        author=request.user).values('id', 'query')
    reviews = Review.objects.filter(user=request.user).order_by('-id')
    bookings = Bookings.objects\
        .prefetch_related('package__activity')\
        .select_related(
            'package__user__profile',
            'package__region',
            'package__category',
            'package__user',
            'package__country',
            'schedule'
        )\
        .filter(
            user=request.user)\
        .order_by('-id')
    on_request_bookings = OnRequestBookings.objects\
        .select_related(
            'package__user__profile',
            'package__region',
            'package__category',
            'package__user',
            'package__country',
        )\
        .prefetch_related('package__activity')\
        .filter(
            user=request.user)\
        .order_by('-id')
    followers = Follow.objects.filter(to_user=request.user)
    followings = Follow.objects.filter(from_user=request.user)
    activities = Activity.objects.values(
        'activity', 'slug').order_by('-id')
    context = {
        'profile': profile,
        'blogs': blogs,
        'saved': saved,
        'queries': queries,
        'reviews': reviews,
        'bookings': bookings,
        'on_request_bookings': on_request_bookings,
        'age': age,
        'followers': followers,
        'followings': followings,
        'activities': activities,
        'form': UserNameForm()
    }
    return render(request, 'users/profile.html', context)


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = [
        'profile_picture',
        'cover_photo',
        'gender',
        'dob',
        'mobile',
        'about',
        'street',
        'house',
        'city',
        'state',
        'country']
    template_name = 'users/create_profile.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = [
        'profile_picture',
        'cover_photo',
        'gender',
        'dob',
        'mobile',
        'about',
        'street',
        'house',
        'city',
        'state',
        'country']
    template_name = 'users/update_profile.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.author:
            return True
        return False


@login_required
def follow(request, pk):
    from_user = request.user
    to_user = User.objects.get(id=pk)
    try:
        followed = Follow.objects.get(from_user=from_user, to_user=to_user)
        if followed.is_follow == True:
            Follow.objects.update(
                from_user=from_user,
                to_user=to_user, is_follow=False)
            data = {
                'success': True,
                'msg': 'Unfollowed'
            }
        else:
            Follow.objects.update(
                from_user=from_user,
                to_user=to_user, is_follow=True)
            data = {
                'success': True,
                'msg': 'Followed'
            }
    except Follow.DoesNotExist:
        Follow.objects.create(
            from_user=from_user,
            to_user=to_user, is_follow=True)
        data = {
            'success': True,
            'msg': 'Followed'
        }
    return JsonResponse(data)


@login_required
def update_name(request):
    form = UserNameForm(request.POST)
    if form.is_valid():
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, 'You have successfully updated your name.')
        return redirect('profile')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('profile')


@login_required
def answers(request, pk):
    answers = serializers.serialize('json', Answer.objects.filter(query=pk))
    answers = json.loads(answers)
    return JsonResponse(answers, safe=False)
