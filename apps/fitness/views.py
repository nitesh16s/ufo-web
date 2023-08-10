from django.contrib import messages
from .models import Program, ProgramBooking
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from .forms import ProgramBookingForm


class ProgramListView(View):

    def get(self, request, *args, **kwargs):
        programs = Program.objects.select_related()
        context = {
            'programs': programs
        }
        return render(request, 'fitness/programs.html', context)


class ProgramDetailView(View):

    def get(self, request, program_slug, *args, **kwargs):
        program = get_object_or_404(Program, slug=program_slug)
        booking_form = ProgramBookingForm()
        context = {
            'program': program,
            'booking_form': booking_form
        }
        return render(request, 'fitness/program_detail.html', context)


class ProgramBookingView(View):

    def post(self, request, program_slug, *args, **kwargs):
        program = get_object_or_404(Program, slug=program_slug)
        form = ProgramBookingForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            short_message = request.POST.get('short_message')
            obj = ProgramBooking(
                program=program,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                short_message=short_message
            )
            obj.save()
            messages.success(
                request, 'Congrats, Your Fitness Program has been booked. We will connect with you soon.')
            return redirect('fitness_programs')
        else:
            messages.error(request, f'Error {form.errors}')
            return redirect('fitness_program_detail', program_slug)
