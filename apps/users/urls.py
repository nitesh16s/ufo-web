from django.urls import path
from apps.users.views import (
    ProfileCreateView,
    ProfileUpdateView,
    profile,
    follow,
    update_name,
    answers
)

urlpatterns = (
    path('profile/', profile, name='profile'),
    path('create/profile/', ProfileCreateView.as_view(), name='create_profile'),
    path('profile/<str:slug>/update/',
         ProfileUpdateView.as_view(), name='update_profile'),
    path('friendships/<int:pk>/follow/', follow, name='follow'),
    path('update-name/', update_name, name='update_name'),
    path('query/<int:pk>/answers/', answers, name='answers')
)
