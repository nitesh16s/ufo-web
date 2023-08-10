from rest_framework import serializers
from apps.blogs.models import Blog
from apps.packages.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')
    # continent = serializers.ReadOnlyField(source='continent.continent')
    # country = serializers.ReadOnlyField(source='country.country')
    # region = serializers.ReadOnlyField(source='region.region')
    # activity = ActivitySerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = ['title', 'content', 'blog_image', 'activity']
