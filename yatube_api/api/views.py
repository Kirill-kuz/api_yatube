from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .serializers import GroupSerializer, PostSerializer, CommentSerializer

from api.permissions import AuthorOrReadOnly
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Post."""

    permission_classes = [IsAuthenticated, AuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    permission_classes = [IsAuthenticated, AuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
