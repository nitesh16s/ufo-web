from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from .models import WeekendAdventure, WeekendAdventureBooking
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from .forms import WeekendAdventureBookingForm


class WeekendAdventureListView(View):

    def get(self, request, *args, **kwargs):
        weekend_programs = WeekendAdventure.objects.select_related()
        context = {
            'weekend_programs': weekend_programs
        }
        return render(request, 'weekend/weekend_programs.html', context)


class WeekendAdventureDetailView(View):

    def get(self, request, weekend_adventure_slug, *args, **kwargs):
        weekend_program = get_object_or_404(
            WeekendAdventure, slug=weekend_adventure_slug)
        booking_form = WeekendAdventureBookingForm()
        context = {
            'weekend_program': weekend_program,
            'booking_form': booking_form
        }
        return render(request, 'weekend/weekend_program_detail.html', context)


class WeekendAdventureBookingView(View):

    def post(self, request, weekend_adventure_slug, *args, **kwargs):
        weekend_program = get_object_or_404(
            WeekendAdventure, slug=weekend_adventure_slug)
        form = WeekendAdventureBookingForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            short_message = request.POST.get('short_message')
            obj = WeekendAdventureBooking(
                weekend_program=weekend_program,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                short_message=short_message
            )
            obj.save()
            messages.success(
                request, 'Congrats, Your Weekend Adventure Program has been booked. We will connect with you soon.')
            return redirect('weekend_adventures')
        else:
            messages.error(request, f'Error {form.errors}')
            return redirect('weekend_adventure_detail', weekend_adventure_slug)
