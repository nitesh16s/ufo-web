from django.urls import path
from .views import ProgramListView, ProgramDetailView, ProgramBookingView

urlpatterns = [
    path('training-programs', ProgramListView.as_view(), name='fitness_programs'),
    path('training-programs/<program_slug>', ProgramDetailView.as_view(), name='fitness_program_detail'),
    path('program/<program_slug>/booking', ProgramBookingView.as_view(), name='fitness_program_booking')
]