from django.urls import path
from apps.main.views import (
    index, about, contact, search, show_country_packages, show_countries, workwithus,
    activities, adventures, sponsers, show_training_programs,show_weekend_adventures,
    activity_packages, less_explored_packages, perfect_trips, show_less_explored
)

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('show-activities', activities, name='activities'),
    path('show-adventures', adventures, name='adventures'),
    path('activity/<str:slug>', activity_packages, name='activity_packages'),
    path('less-explored', less_explored_packages,
         name='less_explored_packages'),
    path('show-training-programs', show_training_programs,
         name='show_training_programs'),
    path('show-less-explored', show_less_explored, name='show_less_explored'),
    path('show-weekend-adventures', show_weekend_adventures, name='show_weekend_adventures'),
    path('show-countries', show_countries, name='show_countries'),
    path('show-country-packages/<int:country_id>',
         show_country_packages, name='country_packages'),
    path('perfect-trips/<str:entry>', perfect_trips, name='perfect_trips'),
    path('sponsers', sponsers, name='sponsers'),
    path('work-with-us', workwithus, name='work_with_us'),
    path('search', search, name='search')
]
