from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets
from rest_framework import permissions

from reviews.models import User
from .serializers import UserSerializer, SingUpSerializer, GetTokenSerializer
from .permissions import AdminOnly


class SingUpView(APIView):

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
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
            if not created:
                return Response({
                        'username': 'Данный пользователь уже существует',
                        'email': 'Данный пользователь уже существует'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, username=serializer.data['username'])
            if default_token_generator.check_token(
                user=user,
                token=serializer.data['confirmation_code']
            ):
                access = AccessToken.for_user(user)
                data = {
                    'token': str(access)
                }
            else:
                data = {
                    'confirmation_code': 'Указан неверный код подтверждения',
                }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AdminOnly,)
    permission_classes = (permissions.IsAuthenticated,)
