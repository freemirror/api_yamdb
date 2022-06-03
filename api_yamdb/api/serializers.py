import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

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


class SingUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено.'
            )
        elif not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'В username используются запрещенные символы'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()
