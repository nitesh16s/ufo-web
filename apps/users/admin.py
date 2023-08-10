from django.contrib import admin
from apps.users.models import Profile, Team, Follow

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Follow)