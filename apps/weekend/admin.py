import django
from django.contrib import admin
from .models import WeekendAdventure, WeekendAdventureBooking


admin.site.register(WeekendAdventure)
admin.site.register(WeekendAdventureBooking)
