from apps.weekend.models import WeekendAdventure, WeekendAdventureBooking
from django.urls import path
from .views import WeekendAdventureListView, WeekendAdventureDetailView, WeekendAdventureBookingView


urlpatterns = [
    path('weekend-adventures', WeekendAdventureListView.as_view(),
         name='weekend_adventures'),
    path('weekend-adventure/<weekend_adventure_slug>',
         WeekendAdventureDetailView.as_view(), name='weekend_adventure_detail'),
    path('weekend-adventure/<weekend_adventure_slug>/booking',
         WeekendAdventureBookingView.as_view(), name='weekend_adventure_booking')
]
