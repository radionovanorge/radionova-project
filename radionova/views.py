import datetime
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post
# from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer

# from .pagination import CustomPagination
# from .filters import LocationFilter


class ListCreatePostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyPostAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

