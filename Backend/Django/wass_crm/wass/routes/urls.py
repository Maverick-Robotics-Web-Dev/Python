from rest_framework.routers import DefaultRouter

from models.settings.branch_offices.views import BranchOfficesViewSet

router: DefaultRouter = DefaultRouter()
router.register('settings/branch-offices', BranchOfficesViewSet, 'branch-offices')
urlpatterns: list = router.urls
