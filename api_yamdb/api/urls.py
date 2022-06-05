from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SingUpView, GetTokenView, UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SingUpView.as_view(), name='sign_up'),
    path('auth/token/', GetTokenView.as_view(), name='get_token'),
    path('', include(router.urls))
]
