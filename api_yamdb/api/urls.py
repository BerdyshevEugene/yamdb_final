from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (AuthViewSet,
                    CategoryViewSet,
                    CommentViewSet,
                    UserViewSet,
                    TitleViewSet,
                    GenreViewSet,
                    ReviewViewSet,)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/auth/signup/', AuthViewSet.sign_up),
    path('v1/auth/token/', AuthViewSet.jwt_token),
    path('v1/', include(router_v1.urls)),
]
