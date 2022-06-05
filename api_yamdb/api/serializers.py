import re

from rest_framework import serializers
from reviews.models import User


class ValidateFunctions:

    def validate_username(self, value):
        if User.objects.filter(username=value).count():
            raise serializers.ValidationError(
                'Указанное имя пользователя уже существует.'
            )
        elif value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.'
            )
        elif not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'В username используются запрещенные символы'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).count():
            raise serializers.ValidationError(
                'Указанный email уже существует.'
            )
        elif not re.match(r'[^@\s]+@[^@\s]+\.[^@\s]+', value):
            raise serializers.ValidationError(
                'Некоректный адресс e-mail'
            )
        return value


class UserSerializer(serializers.ModelSerializer, ValidateFunctions):

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


class OwnUserSerializer(serializers.ModelSerializer, ValidateFunctions):
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(max_length=254, required=False)
    role = serializers.CharField(read_only=True)

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


class SingUpSerializer(serializers.Serializer, ValidateFunctions):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
