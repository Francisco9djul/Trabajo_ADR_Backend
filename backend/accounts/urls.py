from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet ,search_users, UserCreateAPIView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='api-register'),
    path('users/search/', search_users, name='search-users'),
    path('', include(router.urls)),
]
