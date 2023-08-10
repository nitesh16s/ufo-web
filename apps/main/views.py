import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from ..packages.models import Continent, Country, Package, Activity
from apps.blogs.models import Blog
from apps.users.models import Team
from apps.main.models import Query, Sponsers, WorkWithUs
from apps.fitness.models import Program
from apps.weekend.models import WeekendAdventure
from apps.main.forms import QueryForm
from django.core import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from uforangers.mailer import sendmail


# Error handling
def handler404(request, exception):
    return render(request, 'main/404.html', status=404)


def handler500(request):
    return render(request, 'main/500.html', status=500)

# Index page renders


def index(request):
    packages = Package.objects\
        .prefetch_related('activity')\
        .select_related(
            'category',
            'region',
            'country')\
        .all()[:8]
    continents = Continent.objects.values(
        'slug', 'continent', 'image')
    blogs = Blog.objects.select_related().order_by('-id')[:2]
    teams = Team.objects.all()
    context = {
        'packages': packages,
        'continents': continents,
        'blogs': blogs,
        'teams': teams
    }
    return render(request, 'main/index.html', context)


# Nav renders api
# Show packages=>countries
def show_countries(request):
    countries = list(
        Country.objects
        .values(
            'id',
            'slug',
            'country'
        )
    )
    return JsonResponse(countries, content_type='application/json', safe=False)


# show package=>countries=>packages
def show_country_packages(request, country_id):
    packages = list(
        Package.objects
        .values(
            'name',
            'slug',
            'country__slug',
            'region__slug')
        .filter(country=country_id))
    return JsonResponse(packages, content_type='application/json', safe=False)


# about
def about(request):
    return render(request, 'main/about.html')


# contact
def contact(request):
    if request.method == 'GET':
        query_form = QueryForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(
                request, 'You need to login before submitting your query.')
            return redirect('account_login')
        query_form = QueryForm(request.POST)
        if query_form.is_valid():
            query = request.POST.get('query')
            query = Query(query=query, author=request.user)
            query.save()
            # send emails to the admin
            sendmail.delay(
                subject='New Query',
                message=f'{query.query}',
                to='niteshsaini1606@gmail.com'
            )
            sendmail.delay(
                subject='New Query',
                message=f'{query.query}',
                to='rk9080835@gmail.com'
            )
            query_form = QueryForm()
            messages.success(
                request, 'Your query has been submitted. We\'ll reply you soon.')
    return render(request, 'main/contact.html', {'query_form': query_form})


# nav=>activity=>showactivity
def activities(request):
    activities = Activity.objects.all()
    activities = serializers.serialize('json', list(
        activities), fields=['activity', 'slug', 'pk'])
    activities = json.loads(activities)
    data = []
    for activity in activities:
        activity = {
            'id': activity['pk'],
            'fields': activity['fields']
        }
        data.append(activity)
    return JsonResponse(data, content_type='application/json', safe=False)


# nav=>training-programs
def show_training_programs(request):
    programs = list(
        Program.objects
        .values(
            'name',
            'slug'
        ))
    return JsonResponse(programs, safe=False)


# nav=>less-explored-packages
def show_less_explored(request):
    packages = list(
        Package.objects
        .values(
            'name',
            'slug',
            'country__slug',
            'region__slug')
        .filter(is_less_explored_region=True))
    return JsonResponse(packages, safe=False)


# nav=>adventures-in=>show-adventures
def adventures(request):
    adventures = Continent.objects.all()
    adventures = serializers.serialize('json', list(
        adventures), fields=['continent', 'slug', 'pk'])
    adventures = json.loads(adventures)
    data = []
    for adventure in adventures:
        adventure = {
            'id': adventure['pk'],
            'fields': adventure['fields']
        }
        data.append(adventure)
    return JsonResponse(data, content_type='application/json', safe=False)


# nav=>activities=>packages based on slug
def activity_packages(request, slug):
    try:
        activity = Activity.objects.get(slug=slug)
    except Activity.DoesNotExist:
        return HttpResponse('Invalid Activity')
    packages = Package.objects\
        .prefetch_related('activity')\
        .select_related(
            'region',
            'category',
            'country',
            'dailyuseitem',
            'fitnessguide',
            'itinerary',
            'detaileditinerary',
            'packageinclution',
            'packageexclution',
            'faq')\
        .filter(activity=activity.id)
    blogs = Blog.objects.filter(activity=activity.id)
    context = {
        'activity': activity,
        'packages': packages,
        'blogs': blogs,
    }
    return render(request, 'main/activity.html', context)


# less explored
def less_explored_packages(request):
    less_explored_packages = Package.objects\
        .prefetch_related('activity')\
        .select_related(
            'region',
            'category',
            'country',
            'dailyuseitem',
            'fitnessguide',
            'itinerary',
            'detaileditinerary',
            'packageinclution',
            'packageexclution',
            'faq')\
        .filter(
            is_less_explored_region=True)
    return render(request, 'main/less_explored_packages.html',
                  {'less_explored_packages': less_explored_packages})


# weekend adventure
def show_weekend_adventures(request):
    weekend_adventures = list(WeekendAdventure.objects.values('name', 'slug'))
    return JsonResponse(data=weekend_adventures, content_type='application/json', safe=False)


# Index page search
def perfect_trips(request, entry):
    packages = list(
        Package.objects
        .values(
            'name',
            'slug',
            'country__slug',
            'region__slug')
        .filter(name__icontains=entry))
    return JsonResponse(packages, content_type='application/json', safe=False)


# Sponsers
def sponsers(request):
    sponsers = list(Sponsers.objects.values('name', 'image', 'url'))
    return JsonResponse(sponsers, safe=False)


# work with us
def workwithus(request):
    email = request.POST.get('email')
    try:
        validate_email(email)
    except ValidationError as e:
        messages.warning(request, e)
        return redirect('index')

    if WorkWithUs.objects.filter(email=email).exists():
        messages.warning(request, 'We already have your email.')
        return redirect('index')

    applier = WorkWithUs(email=email)
    applier.save()

    # shoot the admin an email
    sendmail.delay(
        subject='Work with us.',
        message=f'{email} wants to work with us.',
        to='rk9080835@gmail.com'
    )
    messages.info(request, 'We got your email. We will contact you soon.')
    return redirect('index')


# search results
def search(request):
    query = request.GET['q']
    packages = Package.objects\
        .prefetch_related('activity')\
        .select_related(
            'region',
            'category',
            'country',
            'dailyuseitem',
            'fitnessguide',
            'itinerary',
            'detaileditinerary',
            'packageinclution',
            'packageexclution',
            'faq')\
        .filter(name__icontains=query)
    return render(request, 'main/search_results.html', {'packages': packages})
