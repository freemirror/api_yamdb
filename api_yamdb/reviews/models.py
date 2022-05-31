from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(blank=True)
    rating = models.IntegerField(blank=True)
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        null=True, blank=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles',
        null=True, blank=True
    )

    def __str__(self):
        return self.name
