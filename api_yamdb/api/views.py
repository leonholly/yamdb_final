from django.db.models import Count, Sum
from django.db.models.functions import Round
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Genre, Title
from users.permissions import AdminOrReadOnly, AuthorPermission

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTitleSerializer,
                          ReviewSerializer, TitleSerializer)


class GetCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(GetCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Round(Sum('reviews__score') / Count('reviews'))
    ).order_by(
        'name'
    ).select_related(
        'category'
    ).prefetch_related(
        'genre'
    )
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermission
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermission
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(title.reviews.all(), id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(title.reviews.all(), id=review_id)
        serializer.save(
            review=review,
            author=self.request.user
        )
