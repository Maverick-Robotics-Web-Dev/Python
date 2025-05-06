from rest_framework.routers import DefaultRouter

from models.users.views import UserViewSet

router: DefaultRouter = DefaultRouter()
router.register(prefix='users', viewset=UserViewSet, basename='users')
urlpatterns: list = router.urls
