from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.blogs.serializers import BlogSerializer
from apps.blogs.models import Blog


class BlogView(APIView):
    '''
    View for list all blogs, or create a new blog.
    '''

    def get(self, request, format=None):
        blogs = Blog.objects.prefetch_related('activity').select_related()
        serializer = BlogSerializer(blogs, many=True)
        print(serializer)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.user)
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailView(APIView):
    """
    View for retrieve, update or delete a blog instance.
    """

    def get_object(self, pk):
        try:
            return Blog.objects.get(id=pk)
        except Blog.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     blog = self.get_object(pk)
    #     blog.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
