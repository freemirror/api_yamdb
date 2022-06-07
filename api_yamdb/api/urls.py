from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    GenreViewSet, CommentViewSet, ReviewViewSet,
    CategoryViewSet, TitleViewSet, SingUpView, GetTokenView, UsersViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/signup/', SingUpView.as_view(), name='sign_up'),
    path('auth/token/', GetTokenView.as_view(), name='get_token'),
    # path('', include(router.urls))
]
