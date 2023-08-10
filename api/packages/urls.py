from django.urls import path, include
from api.packages.views import (
    ActivityView,  PackageView, PackageDetailView, PackageGalleryView, ReviewView, BookingView
)

urlpatterns = [
    path('packages/', PackageView.as_view()),
    path('package/<int:pk>/', PackageDetailView.as_view()),
    path('package/<int:pk>/gallery/', PackageGalleryView.as_view()),
    path('package/<int:pk>/review/', ReviewView.as_view()),
    path('package/<int:package_id>/<int:schedule_id>/booking/',
         BookingView.as_view()),
    path('activity/', ActivityView.as_view()),
    # path('package/', package_api)
]
