from api_yamdb.settings import EMAIL_FROM

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import viewsets, permissions, status, filters
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken


from reviews.models import User, Category, Genre, Title, Review
from .filters import TitleFilter
from .mixins import CDLMixinViewSet
from .permissions import (AdminModeratorAuthorPermission,
                          IsAdminSuperOrReadOnly, UserRead)
from .serializers import (AuthSerializer, AuthTokenSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, TitlePostSerializer,
                          TitleGetSerializer, ReviewSerializer,
                          UsersSerializer)


class UserViewSet(viewsets.ModelViewSet):
    '''Реализация операций с моделью пользователей:
    - получение списка пользователей
    - добавление пользователя
    - получение пользователя
    - изменение данных пользователя
    - удаление пользователя
    - получение/изменение данных учетной записи.'''
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, UserRead)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch',),
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method != 'PATCH':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UsersSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.user.role == (user.is_staff
                                      or self.request.user.is_superuser):
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


class AuthViewSet(viewsets.ModelViewSet):
    '''Регистрация пользователей и выдача токенов.'''
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def sign_up(request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        exist_mail = User.objects.filter(email=email).exists()
        exist_user = User.objects.filter(username=username).exists()
        if exist_user or exist_mail:
            return Response('Имя пользователя или данные уже заняты',
                            status=status.HTTP_400_BAD_REQUEST)
            # без статуса 400, тесты не проходит
        try:
            user = User.objects.get_or_create(
                username=username,
                email=email
            )[0]
        except NameError:
            Response('Имя пользователя или данные уже заняты',
                     status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Токен',
            message=f'Токен: {confirmation_code}',
            from_email=EMAIL_FROM,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def jwt_token(request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        error = {'ошибка': 'код некорректный'}
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_200_OK)
        else:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CDLMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminSuperOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CDLMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminSuperOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('-name')
    serializer_class = TitleGetSerializer
    permission_classes = (IsAdminSuperOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
