from django import forms
from django.forms.widgets import ClearableFileInput
from .models import ProgramBooking


class ProgramBookingForm(forms.ModelForm):
    class Meta:
        model = ProgramBooking
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'short_message']

