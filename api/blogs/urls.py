from django.urls import path
from api.blogs.views import BlogView, BlogDetailView

urlpatterns = [
    path('blogs/', BlogView.as_view()),
    path('blog/<int:pk>/', BlogDetailView.as_view()),
]