from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User
from .permissions import AdminOnly
from .serializers import (
    UserSerializer,
    SingUpSerializer,
    GetTokenSerializer,
    OwnUserSerializer
)


class SingUpView(APIView):

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.data['username'],
                email=serializer.data['email']
            )
            token = default_token_generator.make_token(user=user)
            send_mail(
                'SingUp in Yamdb',
                f'Confirmation code: {token}',
                'post@mail.ru',
                [user.email, ]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            if default_token_generator.check_token(
                user=user,
                token=serializer.data['confirmation_code']
            ):
                access = AccessToken.for_user(user)
                data = {'token': str(access)}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'confirmation_code': 'Указан неверный код подтверждения',
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        serializer_class=OwnUserSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
