from rest_framework import serializers
from django.db.models import Avg
import datetime as dt
from reviews.models import GenreTitle
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Genre, Title, Category, User, Comment, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre =  serializers.SlugRelatedField(
        required=False,
        slug_field='slug',
        many=True,
        # queryset=Category.objects.all()
        read_only=True
    )
    category = serializers.SlugRelatedField(
        required=False,
        slug_field='slug',
        # queryset=Category.objects.all()
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        value = Review.objects.filter(
            title=obj.id
        ).aggregate(rating=Avg('score'))
        return value['rating']

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год рождения!')
        return value


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
