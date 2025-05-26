from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet
from apps.authentication.views import AuthViewSet


router: DefaultRouter = DefaultRouter()
router.register(prefix='auth', viewset=AuthViewSet, basename='auth')
router.register(prefix='users', viewset=UserViewSet, basename='users')
urlpatterns: list = router.urls
