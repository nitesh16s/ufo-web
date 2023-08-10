from django import forms
from .models import WeekendAdventureBooking


class WeekendAdventureBookingForm(forms.ModelForm):
    class Meta:
        model = WeekendAdventureBooking
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'short_message']
