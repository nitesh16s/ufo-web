import debug_toolbar
from django.contrib import admin, sitemaps
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache
from apps.main.views import handler404, handler500

# sitemap
from django.contrib.sitemaps.views import sitemap
from apps.packages.sitemaps import (
    IndexSiteMap,
    CountrySiteMap,
    StaticSiteMap,
    ContinentSiteMap,
    ActivitySiteMap,
    PackageSiteMap,
    BlogSiteMap
)

# local app urls
from apps.users import urls as users_urls
from apps.blogs import urls as blogs_urls
from apps.main import urls as main_urls
from apps.packages import urls as packages_urls
from apps.allauth import urls as allauth_urls
from apps.fitness import urls as fitness_urls
from apps.weekend import urls as weekend_urls


# api urls
from api.blogs import urls as api_blog_urls
from api.packages import urls as api_package_urls

# swagger urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="UFORangers API",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
)

sitemaps = {
    'index': IndexSiteMap,
    'static': StaticSiteMap,
    'continents': ContinentSiteMap,
    'countries': CountrySiteMap,
    'activity': ActivitySiteMap,
    'packages': PackageSiteMap,
    'blogs': BlogSiteMap
}

urlpatterns = [
    # sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # admin panel
    path('uforangers-dashboard/', admin.site.urls),

    # urls for local apps
    path('accounts/', include(allauth_urls)),
    path('', include(weekend_urls)),
    path('', include(blogs_urls)),
    path('', include(main_urls)),
    path('', include(fitness_urls)),
    path('', include(packages_urls)),
    path('accounts/', include(users_urls)),

    # api urls
    path('api/', include(api_blog_urls)),
    path('api/', include(api_package_urls)),

    # urls for third party apps
    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse),
         name='ckeditor_browse'),
    path('__debug__/', include(debug_toolbar.urls)),

    # api documentation urls
    path('swagger/json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
