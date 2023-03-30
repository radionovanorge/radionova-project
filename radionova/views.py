from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []
    filterset_fields = [
        "id",
        "content",
        "created",
        "updated",
        "heading",
        "author",
        "program",
    ]
