from django import forms
from django.forms.widgets import ClearableFileInput
from apps.packages.models import (
    Bookings,
    OnRequestBookings,
    Review,
    PackageGallery
)
from bootstrap_datepicker_plus import DateTimePickerInput


class ImageForm(forms.ModelForm):
    class Meta:
        model = PackageGallery
        fields = ['package', 'image']
        widgets = {
            'image': ClearableFileInput(attrs={
                'multiple': True
            }),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['seat_count', 'phone_number', 'is_read']


class OnRequestBookingForm(forms.ModelForm):
    class Meta:
        model = OnRequestBookings
        fields = ['month', 'seat_count', 'phone_number', 'short_message', 'is_read']
        # widgets = {
        #     # default date-format %m/%d/%Y will be used
        #     'start_date': DateTimePickerInput(format='%Y-%m-%d'),
        #     # specify date-frmat
        #     'end_date': DateTimePickerInput(format='%Y-%m-%d'),
        # }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
