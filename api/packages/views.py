import json
import re
from django.db.models import fields
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from api.packages.serializers import (
    ActivitySerializer,
    PackageSerializer,
    ImageSerializer,
    ReviewSerializer,
    BookingSerializer
)
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication
from apps.packages.models import (
    Activity,
    Package,
    PackageGallery,
    Review,
    Bookings
)
from django.core import serializers


class ActivityView(APIView):

    '''
    List all activities,  or create a new activity.
    '''

    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageView(APIView):
    '''
    List all packages, or create a new package
    '''

    def get(self, request, format=None):
        packages = Package.objects.prefetch_related(
            'activity').select_related()
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        post_data = request.data
        post_data['slug'] = 'testing'
        serializer = PackageSerializer(data=post_data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageDetailView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        package = Package.objects\
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
                'faq'
            )\
            .prefetch_related('activity').get(id=pk)
        serializer = PackageSerializer(package)
        return Response(serializer.data)


class PackageGalleryView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        images = PackageGallery.objects.select_related(
            'package').filter(package_id=pk)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class ReviewView(APIView):

    '''
    List all reviews, or create new review.
    '''

    def get(self, request, pk=None, format=None):
        package = Package.objects.get(id=pk)
        reviews = Review.objects.filter(
            package=package).select_related('user__profile')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None, format=None):
        user = self.request.user
        package = get_object_or_404(Package, id=pk)
        data = {}
        data['user'] = user.id
        data['package'] = package.id
        data['rating'] = request.data['rating']
        data['content'] = request.data['content']
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingView(APIView):
    '''
    Booking View => Takes package_id, schedule_id
    '''

    def get(self, request, package_id=None, schedule_id=None, *args, **kwargs):
        user = self.request.user
        bookings = Bookings.objects.filter(
            package_id=package_id, schedule_id=schedule_id)
        print(bookings)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, package_id, schedule_id):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def package_api(request):
#     packages = Package.objects.all()
#     packages = serializers.serialize(
#         'json', packages, use_natural_foreign_keys=True)
#     packages = json.loads(packages)
#     return JsonResponse(packages, content_type='application/json', safe=False)