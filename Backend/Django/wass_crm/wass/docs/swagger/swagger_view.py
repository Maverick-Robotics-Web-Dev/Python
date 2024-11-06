from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="WASS API",
        default_version='v1',
        description="Es para softwares contables y de market",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mavroboticswebdev7690@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
