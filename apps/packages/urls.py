from django.urls import path
from .views import (
    PackageListView,
    PackageCreateView,
    PackageDetailView,
    CreatePackageReview,
    BookingCreateView,
    OnRequestBookingCreateView,
    confirm_payment,
    bank_details,
    uploadimages,
    showGallery,
    availableSeats,
    region_packages,
    continent,
    country_packages
)

urlpatterns = [
    path('payment', bank_details, name='bank_details'),
    path('packages', PackageListView.as_view(), name='packages'),
    path('new/package', PackageCreateView.as_view(), name='create_package'),
    path('explore/<str:slug>', continent, name='continent'),
    path('<str:slug>', country_packages, name='country_packages'),
    path('<str:country>/<str:region>',
         region_packages, name='region_packages'),
    path('<str:country>/<str:region>/<str:package_name>',
         PackageDetailView.as_view(), name='package_detail'),
    path('packages/<int:package_id>/<int:schedule_id>/available-seats',
         availableSeats, name='available-seats'),
    path('<str:country>/<str:region>/<str:package_name>/<int:schedule_id>/book',
         BookingCreateView.as_view(), name='book_package'),
    path('<str:country>/<str:region>/<str:package_name>/on-request-booking',
         OnRequestBookingCreateView.as_view(), name='on_request_booking'),
    path('confirm-payment', confirm_payment, name='confirm_payment'),
    path('packages/<str:slug>/new/review',
         CreatePackageReview.as_view(), name='reviews'),
    path('upload-multiple', uploadimages, name='add_images'),
    path('gallery/<int:package_id>', showGallery, name='show_gallery'),
]