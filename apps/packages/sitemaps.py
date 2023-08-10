from apps.blogs.models import Blog
from django.contrib.sitemaps import Sitemap
from django.urls.base import reverse
from .models import (
    Activity, Package, Country, Continent
)


class IndexSiteMap(Sitemap):
    protocol = 'https'
    priority = 1.0

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class StaticSiteMap(Sitemap):
    protocol = 'https'
    priority = 0.8

    def items(self):
        return [
            'packages',
            'fitness_programs',
            'less_explored_packages',
            'blogs',
            'contact',
            'account_signup',
            'account_login',
            'about',
        ]

    def location(self, item):
        return reverse(item)


class ContinentSiteMap(Sitemap):
    protocol = 'https'
    priority = 0.64

    def items(self):
        return Continent.objects.all()

    def location(self, obj: Continent) -> str:
        return super().location(obj)


class CountrySiteMap(Sitemap):
    protocol = 'https'
    priority = 0.64

    def items(self):
        return Country.objects.all()

    def location(self, obj: Country) -> str:
        return super().location(obj)


class ActivitySiteMap(Sitemap):
    protocol = 'https'
    priority = 0.80

    def items(self):
        return Activity.objects.all()

    def location(self, obj: Activity) -> str:
        return obj.get_absolute_url_packages()


class PackageSiteMap(Sitemap):
    protocol = 'https'
    priority = 0.80

    def items(self):
        return Package.objects.all()

    def lastmod(self, obj):
        return obj.createdAt

    def location(self, obj: Package) -> str:
        return super().location(obj)


class BlogSiteMap(Sitemap):
    protocol = 'https'
    priority = 0.64

    def items(self):
        return Activity.objects.all()

    def location(self, obj: Activity) -> str:
        return obj.get_absolute_url_blogs()


class LogoutSiteMap(Sitemap):
    protocol = 'https'
    priotity = 0.5

    def items(self):
        return ['account_logout']

    def location(self, item):
        return reverse(item)
