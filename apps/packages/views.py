# stdlib imports
import json
import time
import threading
import datetime

# core django imports
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from django.contrib import messages
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.views.generic.base import View
from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.core import serializers

# third party packages
import razorpay

# local apps
from .models import (
    Continent,
    Country,
    Package,
    Bookings,
    OnRequestBookings,
    Schedule,
    Review,
    PackageFlexibleCost,
    Region,
    Activity,
    PackageGallery
)
from ..blogs.models import Blog
from .forms import(
    ImageForm,
    BookingForm,
    OnRequestBookingForm,
    ReviewForm
)
from uforangers.mailer import sendmail


def continent(request, slug):
    try:
        continent = get_object_or_404(Continent, slug=slug)
    except Continent.DoesNotExist:
        return HttpResponse('{} has not added'.format(slug))
    countries = Country.objects.filter(continent=continent.id)
    context = {
        'countries': countries,
        'continent': continent,
    }
    return render(request, 'packages/countries.html', context)


def country_packages(request, slug):
    try:
        country = get_object_or_404(Country, slug=slug)
    except Country.DoesNotExist:
        return HttpResponse('{} has not added'.format(slug))

    # main package query
    findPackage = Package.objects\
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
            'faq')

    if request.GET:
        activity = request.GET.get('activity')
        region = request.GET.get('region')

        if activity and not region:
            activity = Activity.objects.get(slug=activity)
            packages = findPackage.filter(
                country=country.id, activity=activity)

        if region and not activity:
            region = Region.objects.get(slug=region)
            packages = findPackage.filter(
                country=country.id, region=region)

        if activity and region:
            activity = Activity.objects.get(slug=activity)
            region = Region.objects.get(slug=region)
            packages = findPackage.filter(
                country=country.id, activity=activity.id)

    else:
        packages = findPackage.filter(country=country.id)

    regions = Region.objects.all()
    activities = Activity.objects.all()
    context = {
        'packages': packages,
        'country': country,
        'regions': regions,
        'activities': activities,
    }
    return render(request, 'packages/country_packages.html', context)


class PackageListView(View):
    '''
    View for listing all the packages present in the database.
    '''

    def get(self, request, *args, **kwargs):
        '''
        If user adding filter on package listing
        then check else show all packages.
        '''

        packageQuery = Package.objects\
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
                'faq')

        if request.GET:
            # Get activity added by user
            activity = request.GET.get('activity')
            # Get region added by user
            region = request.GET.get('region')

            if activity and not region:
                activity = Activity.objects.get(slug=activity)
                packages = packageQuery.filter(
                    activity=activity)
                blogs = Blog.objects.select_related().filter(
                    activity=activity)

            if region and not activity:
                region = Region.objects.get(slug=region)
                packages = packageQuery.filter(
                    region=region)
                blogs = Blog.objects.select_related().filter(region=region)

            if activity and region:
                activity = Activity.objects.get(slug=activity)
                region = Region.objects.get(slug=region)
                packages = packageQuery.filter(
                    region=region, activity=activity)
                blogs = Blog.objects.select_related().filter(
                    activity=activity, region=region)
        else:
            '''
            If no filter show all data. Later add pagination.
            '''
            packages = packageQuery
            blogs = Blog.objects.select_related().filter()

        regions = Region.objects.all()
        activities = Activity.objects.all()

        context = {
            'packages': packages,
            'regions': regions,
            'activities': activities,
            'blogs': blogs,
        }
        return render(request, 'packages/packages.html', context)


class PackageCreateView(LoginRequiredMixin, CreateView):
    '''
    View for adding new package to the database.
    '''
    model = Package
    fields = [
        'region',
        'activity',
        'category',
        'country',
        'package_image',
        'package_cover',
        'name',
        'about',
        'currency',
        'original_cost',
        'group_cost',
        'difficulty',
        'duration',
        'start_point',
        'end_point',
        'group_size',
        'min_age',
        'max_alt',
        'best_season',
        'walking',
        'is_weekend_adventure',
        'is_training_program',
        'is_less_explored_region',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PackageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    View for updating package.
    '''
    model = Package
    fields = [
        'region',
        'activity',
        'category',
        'country',
        'package_image',
        'package_cover',
        'name',
        'about',
        'currency',
        'original_cost',
        'group_cost',
        'difficulty',
        'duration',
        'start_point',
        'end_point',
        'group_size',
        'min_age',
        'max_alt',
        'best_season',
        'walking',
        'is_weekend_adventure',
        'is_training_program',
        'is_less_explored_region',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        package = self.get_object()
        if self.request.user == package.author:
            return True
        return False


class PackageDetailView(View):
    '''
    View for showing related data to a single package.
    '''

    def get(self, request, package_name, *args, **kwargs):
        # check if the current package exist or not
        package = get_object_or_404(Package, slug=package_name)

        # fetch related objects
        package = Package.objects\
            .select_related(
                'packagehead',
                'region',
                'category',
                'country',
                'dailyuseitem',
                'fitnessguide',
                'itinerary',
                'detaileditinerary',
                'packageinclution',
                'packageexclution',
                'faq'
            ).get(slug=package_name)

        # get the current package discount
        discount = package.original_cost - package.group_cost

        # get the current package reviews
        reviews = Review.objects.filter(package=package).order_by(
            '-id').select_related('user__profile')

        # Filter all stars
        stars = Review.objects.filter(package=package).values(
            'rating').annotate(stars=Count('rating'))

        # total reviews
        total_reviews = reviews.count()

        # overall ratings filter by rating
        total_ratings = 0
        five_stars, four_stars, three_stars, two_stars, one_star = 0, 0, 0, 0, 0
        for review in reviews:
            if review.rating == 5:
                five_stars += 1
            elif review.rating == 4:
                four_stars += 1
            elif review.rating == 3:
                three_stars += 1
            elif review.rating == 2:
                two_stars += 1
            else:
                one_star += 1
            total_ratings += review.rating
        if total_reviews > 0:
            total_ratings = total_ratings/total_reviews

        # filter schedules from current date
        schedules = Schedule.objects.filter(
            start_date__gte=datetime.date.today(), package=package)

        # flexible costs
        flexible_costs = PackageFlexibleCost.objects.filter(
            package_id=package.id)

        # package gallery
        gallery = PackageGallery.objects.filter(
            package=package).order_by('-id')

        # render all data to the template.
        context = {
            'package': package,
            'discount': discount,
            'reviews': reviews,
            'schedules': schedules,
            'total_reviews': total_reviews,
            'total_ratings': f'{total_ratings:.2f}',
            'five_stars': five_stars,
            'four_stars': four_stars,
            'three_stars': three_stars,
            'two_stars': two_stars,
            'one_star': one_star,
            'flexible_costs': flexible_costs,
            'gallery': gallery,
            'review_form': ReviewForm()
        }
        return render(request, 'packages/package_detail.html', context)


def region_packages(request, country, region):
    country = Country.objects.get(slug=country)
    region = Region.objects.get(slug=region)
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
        .filter(region=region)
    context = {
        'country': country,
        'region': region,
        'packages': packages
    }
    return render(request, 'packages/region_packages.html', context)


def uploadimages(request):
    '''Function for uploading images for the package gallery.'''
    if request.method == 'POST':
        if request.user.is_superuser:
            package_id = int(request.POST['package'])
            package = Package.objects.get(id=package_id)
            imageform = ImageForm(request.POST, request.FILES)
            images = request.FILES.getlist('image')
            if imageform.is_valid():

                start = time.time()

                # multithreading
                def save_image(image):
                    image = PackageGallery(package=package, image=image)
                    image.save()

                allThreads = []

                for image in images:
                    t = threading.Thread(target=save_image, args=[image])
                    t.start()
                    allThreads.append(t)

                for thread in allThreads:
                    thread.join()

                end = time.time()

                print(end-start)

                messages.success(
                    request, 'Images have been added successfully.')
                return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)
        else:
            return HttpResponse('You do not have permission. You need to login as admin.')
    else:
        imageform = ImageForm()
        return render(request, 'packages/addimages.html', {'imageform': imageform})

# def uploadimages(request):
#     '''
#     Function for adding multiple images related to a package.
#     Only package_user can add images.
#     '''
#     if request.method == 'POST':
#         if request.user.is_superuser:
#             package_id = int(request.POST['package'])
#             package = Package.objects.get(id=package_id)
#             imageform = ImageForm(request.POST, request.FILES)
#             images = request.FILES.getlist('image')
#             if imageform.is_valid():
#                 for image in images:
#                     image = PackageGallery(package=package, image=image)
#                     image.save()
#                 messages.success(
#                     request, 'Images have been added successfully.')
#                 return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)
#         else:
#             return HttpResponse('You do not have permission. You need to login as admin.')
#     else:
#         imageform = ImageForm()
#         return render(request, 'packages/addimages.html', {'imageform': imageform})


def availableSeats(request, package_id, schedule_id):
    '''
    Function for fetching available seats for a package
    on schedule selected by user.
    '''
    package = Package.objects.get(id=package_id)     # Get the current package
    schedule = Schedule.objects.get(id=schedule_id)  # Get the schedule.
    booked_seats_count = Bookings.objects.filter(
        package=package,
        schedule=schedule,
        is_confirmed=True)\
        .aggregate(Sum('seat_count'))  # Get the sum of toal seat count.

    if booked_seats_count['seat_count__sum'] == None:
        booked_seats_count['seat_count__sum'] = 0
    available_seats = schedule.seats - booked_seats_count['seat_count__sum']
    data = {
        'available': available_seats
    }
    return JsonResponse(data)


class BookingCreateView(LoginRequiredMixin, View):
    '''
    View for seat booking of a package.
    '''

    def get(self, request, *args, **kwargs):
        form = BookingForm()
        return render(request, 'packages/booking_form.html', {'form': form})

    # def post(self, request, package_name, schedule_id, *args, **kwargs):
    #     package = Package.objects.get(slug=package_name)
    #     schedule = Schedule.objects.get(id=schedule_id)
    #     booked_seats_count = Bookings.objects.filter(
    #         package=package, schedule=schedule).aggregate(Sum('seat_count'))
    #     if booked_seats_count['seat_count__sum'] == None:
    #         booked_seats_count['seat_count__sum'] = 0
    #     available_seats = schedule.seats - \
    #         booked_seats_count['seat_count__sum']
    #     if available_seats > 0:
    #         booking_form = BookingForm(request.POST)
    #         if booking_form.is_valid():
    #             seat_count = request.POST.get('seat_count')
    #             if int(seat_count) > available_seats:
    #                 messages.info(
    #                     request, 'Required seats more than available seats.')
    #                 return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)
    #             booked = request.POST.get('is_booked') or True
    #             read = request.POST.get('is_read')
    #             if seat_count and booked and read:
    #                 # creating booking object...
    #                 booking = Bookings(package=package, schedule=schedule,
    #                                    user=request.user, seat_count=seat_count)
    #                 # start payment
    #                 # flexible_cost = PackageFlexibleCost.objects.filter(
    #                 #     package_id=package.id, person_count_from__lte=seat_count).values('flex_cost') & PackageFlexibleCost.objects.filter(package_id=package.id, person_count_to__gte=seat_count).values('flex_cost')
    #                 flexible_cost = amount = 100
    #                 # if flexible_cost:
    #                 #     flexible_cost = flexible_cost[0]['flex_cost']
    #                 # else:
    #                 #     flexible_cost = package.cost
    #                 # amount = int(flexible_cost)*int(seat_count) * \
    #                 #     25  # 25% of total amount
    #                 # if amount == 0:
    #                 #     messages.error(
    #                 #         request, 'Something went wrong. Inform us.')
    #                 #     return redirect('profile')
    #                 # print(flexible_cost, seat_count, amount)
    #                 currency = 'INR'
    #                 client = razorpay.Client(
    #                     auth=("rzp_test_SRqvDE4o0fKB3W", "CAYraor0SNcDHvL8UeOcoFh3"))
    #                 response = client.order.create(
    #                     dict(amount=amount, currency=currency))
    #                 print(response)
    #                 if response['status'] == 'created':
    #                     context = {
    #                         'order_id': response['id'],
    #                         'amount': response['amount'],
    #                         'currency': response['currency'],
    #                         'booking': booking,
    #                     }
    #                     return render(request, 'packages/payment.html', context)
    #                 messages.success(
    #                     request, 'Your booking has been confirmed.')
    #             else:
    #                 messages.error(request, 'Something went wrong.')
    #         return render(request, 'packages/booking_form.html', {'form': BookingForm()})
    #     else:
    #         messages.info(
    #             request, 'Sorry, No seats available for this schedule')
    #         return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)

    def post(self, request, package_name, schedule_id, *args, **kwargs):
        package = Package.objects.get(slug=package_name)
        schedule = Schedule.objects.get(id=schedule_id)

        booked_seats_count = Bookings.objects.filter(
            package=package, schedule=schedule, is_confirmed=True)\
            .aggregate(Sum('seat_count'))

        if booked_seats_count['seat_count__sum'] == None:
            booked_seats_count['seat_count__sum'] = 0
        available_seats = schedule.seats - \
            booked_seats_count['seat_count__sum']

        if available_seats > 0:
            booking_form = BookingForm(request.POST)

            if booking_form.is_valid():
                seat_count = request.POST.get('seat_count')

                if int(seat_count) > available_seats:
                    messages.info(
                        request, 'Required seats more than available seats.')
                    return render(request, 'packages/booking_form.html', {'form': BookingForm()})

                phone_number = request.POST.get('phone_number')
                read = request.POST.get('is_read')

                if seat_count and phone_number and read:
                    # creating booking object...
                    booking = Bookings(
                        package=package,
                        schedule=schedule,
                        user=request.user,
                        seat_count=seat_count,
                        phone_number=phone_number,
                        is_read=True)
                    booking.save()

                    # send mails to package-user and booking-user
                    # package-user emailaddress
                    p_email = User.objects.get(id=package.user.id).email

                    # booking-user emailaddress
                    b_email = User.objects.get(id=request.user.id).email

                    sendmail.delay(
                        subject='New Booking.',
                        message=f'{request.user} booked {seat_count} seats for your package {package.name} for schedule {schedule}',
                        to=p_email
                    )
                    sendmail.delay(
                        subject='Booking Created.',
                        message=f'Hey {request.user}, Your booking for {package.name} for schedule {schedule} has been created successfully. Package provider will contact you soon for confirmation and payment related queries.',
                        to=b_email
                    )

                    messages.success(
                        request, 'Success, Booking has been requested.\
                             After payment it will be confirmed.')
                    return redirect('bank_details')
                else:
                    messages.error(
                        request, 'Something went wrong. Kindly fill all the fields of the form.')
            return render(request, 'packages/booking_form.html', {'form': BookingForm()})
        else:
            messages.info(
                request, 'Sorry, No seats available for this schedule')
            return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)


class OnRequestBookingCreateView(LoginRequiredMixin, CreateView):
    '''
    View for booking according to user provided schedules.
    '''

    def get(self, request, *args, **kwargs):
        form = OnRequestBookingForm()
        return render(request, 'packages/booking_form.html', {'form': form})

    def post(self, request, package_name, *args, **kwargs):
        package = Package.objects.get(slug=package_name)
        form = OnRequestBookingForm(request.POST)

        if form.is_valid():
            month = request.POST.get('month')
            phone_number = request.POST.get('phone_number')
            seat_count = request.POST.get('seat_count')
            short_message = request.POST.get('short_message')
            is_read = request.POST.get('is_read')

            if month and seat_count and phone_number and is_read:
                booking = OnRequestBookings(
                    package=package,
                    user=request.user,
                    month=month,
                    seat_count=seat_count,
                    phone_number=phone_number,
                    short_message=short_message,
                    is_read=True)
                booking.save()

                # send mails to package-user and booking-user
                # package-user emailaddress
                p_email = User.objects.get(id=package.user.id).email

                # booking-user emailaddress
                b_email = User.objects.get(id=request.user.id).email

                sendmail.delay(
                    subject='New OnRequest Booking.',
                    message=f'{request.user} booked {seat_count} seats for your package {package.name} for month {month}',
                    to=p_email
                )
                sendmail.delay(
                    subject='Booking Created.',
                    message=f'Hey {request.user}, Your onrequest booking for {package.name} for month {month} has been created successfully. Package provider will contact you soon for confirmation and payment related queries.',
                    to=b_email
                )

                messages.success(
                    request, 'Success, Booking has been requested. \
                        After payment it will be confirmed.')
                return redirect('bank_details')
            else:
                messages.error(
                    request, 'Something went wrong. Kindly fill all fields.')
                return render(
                    request, 'packages/booking_form.html',
                    {'form': OnRequestBookingForm()})

        else:
            messages.error(request, form.errors)
            return render(
                request, 'packages/booking_form.html',
                {'form': OnRequestBookingForm()})


def bank_details(request):
    return render(request, 'packages/bank_details.html')

    # def post(self, request, slug, schedule_id, *args, **kwargs):
    #     package = Package.objects.get(slug=slug)
    #     schedule = Schedule.objects.get(id=schedule_id)
    #     booked_seats_count = Bookings.objects.filter(
    #         package=package, schedule=schedule).aggregate(Sum('seat_count'))
    #     if booked_seats_count['seat_count__sum'] == None:
    #         booked_seats_count['seat_count__sum'] = 0
    #     available_seats = schedule.seats - \
    #         booked_seats_count['seat_count__sum']
    #     if available_seats > 0:
    #         booking_form = BookingForm(request.POST)
    #         if booking_form.is_valid():
    #             seat_count = request.POST.get('seat_count')
    #             if int(seat_count) > available_seats:
    #                 messages.info(
    #                     request, 'Required seats more than available seats.')
    #                 return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)
    #             booked = request.POST.get('is_booked')
    #             read = request.POST.get('is_read')
    #             if seat_count and booked and read:
    #                 # creating booking object...
    #                 booking = Bookings(package=package, schedule=schedule,
    #                                    user=request.user, seat_count=seat_count)
    #                 # start payment
    #                 flexible_cost = PackageFlexibleCost.objects.filter(
    #                     package_id=package.id, person_count_from__lte=seat_count).values('flex_cost') & PackageFlexibleCost.objects.filter(package_id=package.id, person_count_to__gte=seat_count).values('flex_cost')
    #                 if flexible_cost:
    #                     flexible_cost = flexible_cost[0]['flex_cost']
    #                 else:
    #                     flexible_cost = package.cost
    #                 amount = int(flexible_cost)*int(seat_count) * \
    #                     25  # 25% of total amount
    #                 if amount == 0:
    #                     messages.error(
    #                         request, 'Something went wrong. Inform us.')
    #                     return redirect('profile')
    #                 print(flexible_cost, seat_count, amount)
    #                 currency = 'INR'
    #                 client = razorpay.Client(
    #                     auth=("rzp_test_CrsF7yJXz4pFhE", "3g884qpfrjTZ8hWcRe85mhJ3"))
    #                 response = client.order.create(
    #                     dict(amount=amount, currency=currency))
    #                 if response['status'] == 'created':
    #                     context = {
    #                         'order_id': response['id'],
    #                         'amount': response['amount'],
    #                         'currency': response['currency'],
    #                         'booking': booking,
    #                     }
    #                     return render(request, 'packages/payment.html', context)
    #                 messages.success(
    #                     request, 'Your booking has been confirmed.')
    #             else:
    #                 messages.error(request, 'Something went wrong.')
    #         return render(request, 'packages/booking_form.html', {'form': BookingForm()})
    #     else:
    #         messages.info(
    #             request, 'Sorry, No seats available for this schedule')
    #         return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)


def confirm_payment(request):
    data = request.POST
    package = Package.objects.get(id=data['package_id'])
    schedule = Schedule.objects.get(id=data['schedule_id'])
    seat_count = data['seat_count']
    razorpay_payment_id = data['razorpay_payment_id']
    confirm_booking = Bookings(user=request.user, package_id=package.id, schedule_id=schedule.id,
                               seat_count=seat_count, is_read=True)
    confirm_booking.save()
    messages.success(request, 'Congrats, Your booking has been confirmed.')
    return redirect('profile')
    # client = razorpay.Client(
    #     auth=("rzp_test_CrsF7yJXz4pFhE", "3g884qpfrjTZ8hWcRe85mhJ3"))
    # razorpay_dict = {
    #     'razorpay_payment_id': data['razorpay_payment_id'],
    #     'razorpay_order_id': data['razorpay_order_id'],
    #     'razorpay_signature': data['razorpay_signature']
    # }
    # status = client.utility.verify_payment_signature(razorpay_dict)
    # print(status)


class CreatePackageReview(LoginRequiredMixin, View):
    '''
    View for creating reviews
    Check if user purchased package or not.
    Check if user already added review or not.
    '''

    def get(self, request, slug, *args, **kwargs):
        package = Package.objects.get(slug=slug)
        reviews = Review.objects.filter(package=package)
        context = {
            'reviews': reviews,
        }
        return render(request, 'packages/reviews.html', context)

    def post(self, request, slug, *args, **kwargs):
        package = Package.objects.get(slug=slug)
        user = self.request.user

        if Review.objects.filter(package=package, user=user).exists():
            messages.success(
                request, 'Thanks. You have already given your review.')
            return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)

        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            rating = request.POST.get('rating')
            content = request.POST.get('content')
            Review.objects.create(
                package=package, user=request.user, rating=rating, content=content)
            messages.success(request, 'Thanks for your review.')
            return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)

        else:
            messages.error(request, 'Invalid rating provided')
            return redirect('package_detail', country=package.country.slug, region=package.region.slug, package_name=package.slug)


def showGallery(request, package_id):
    gallery = PackageGallery.objects.filter(package=package_id)
    gallery = serializers.serialize(
        'json', gallery, fields=['image'])
    gallery = json.loads(gallery)
    return JsonResponse(data=gallery, safe=False)
