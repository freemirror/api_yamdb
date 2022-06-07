from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.settings import CHOICES_SCORE, ROLE_CHOICES


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        through='GenreTitle'
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class User(AbstractUser):
    password = models.CharField(_('password'), max_length=128, blank=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    bio = models.TextField(blank=True,)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        choices=CHOICES_SCORE
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]



