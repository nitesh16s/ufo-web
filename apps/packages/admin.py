from django.contrib import admin
from apps.packages.models import (
    Continent,
    Country,
    CountryHead,
    Package,
    PackageHead,
    Schedule,
    Itinerary,
    DetailedItinerary,
    PackageGallery,
    FAQ,
    FitnessGuide,
    PackageInclution,
    DailyUseItem,
    Activity,
    ActivityHead,
    Region,
    Review,
    Bookings,
    Category,
    PackageFlexibleCost,
    PackageExclution,
    OnRequestBookings
)

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(CountryHead)
admin.site.register(Package)
admin.site.register(PackageHead)
admin.site.register(Itinerary)
admin.site.register(DetailedItinerary)
admin.site.register(DailyUseItem)
admin.site.register(FitnessGuide)
admin.site.register(PackageInclution)
admin.site.register(FAQ)
admin.site.register(PackageGallery)
admin.site.register(Schedule)
admin.site.register(Activity)
admin.site.register(ActivityHead)
admin.site.register(Region)
admin.site.register(Review)
admin.site.register(Bookings)
admin.site.register(Category)
admin.site.register(PackageFlexibleCost)
admin.site.register(PackageExclution)
admin.site.register(OnRequestBookings)