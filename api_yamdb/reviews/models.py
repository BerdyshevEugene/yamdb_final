from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year

Admin = 'admin'
Moderator = 'moderator'
User = 'user'

Role = [
    (Admin, 'Админ'),
    (Moderator, 'Модератор'),
    (User, 'Пользователь'),
]


class User(AbstractUser):
    """Класс пользователя"""
    username = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    first_name = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    email = models.EmailField(
        db_index=True,
        max_length=30,
        unique=True,
        null=False,
        blank=False
    )
    bio = models.CharField(
        max_length=300,
        blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=Role,
        default=User,
        blank=False
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.is_superuser or self.role == Admin

    @property
    def is_moderator(self):
        return self.role == Moderator

    @property
    def is_user(self):
        return self.role == User

    def __str__(self):
        return self.username


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='уникальный адрес категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='уникальное название жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""
    name = models.CharField(
        max_length=200,
        verbose_name='Произведение',
        db_index=True)
    year = models.PositiveSmallIntegerField(
        verbose_name='год',
        validators=(validate_year,),
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанры'
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв на произведения"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', ],
                name='unique_review'
            )]

    def __str__(self):
        return f'{self.pk}: {self.text[:30]}'


class Comment(models.Model):
    """Комментарии к отзывам, привязан к определённому отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.pk}: {self.text[:30]}'
