from rest_framework import serializers
from apps.packages.models import (
    Activity,
    Package,
    PackageGallery,
    Review,
    Bookings
)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity', 'image']


class PackageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    region = serializers.CharField(source='region.region')
    category = serializers.CharField(source='category.category')
    country = serializers.CharField(source='country.country')
    activity = ActivitySerializer(many=True)

    class Meta:
        model = Package
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageGallery
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    package_rating = serializers.ReadOnlyField(source='get_rating_display')
    profile_pic = serializers.ReadOnlyField(
        source='user.profile.profile_picture.url')

    class Meta:
        model = Review
        fields = '__all__'
        # fields = ['user', 'package', 'rating', 'content', 'profile_pic', 'package_rating', 'author']


class BookingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bookings
        fields = '__all__'
