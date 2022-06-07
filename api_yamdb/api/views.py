from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Genre, Title, Category, Review, User
from .permissions import SpecialPermission, AdminOnly
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    SingUpSerializer,
    GetTokenSerializer,
    OwnUserSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields  = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields  = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(slug=self.request.data.get('category'))
        print(category, '\n\n\n')
        serializer.save(category=category)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (SpecialPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get("review_id")
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (SpecialPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get("title_id")
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
