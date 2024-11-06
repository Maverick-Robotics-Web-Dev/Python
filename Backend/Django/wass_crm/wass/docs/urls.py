from django.urls import (
    URLPattern,
    URLResolver
)

from .coreapi.coreapi_urls import url_coreapi
from .swagger.swagger_urls import url_swagger


urlpatterns: list[URLResolver | URLPattern] = url_swagger + url_coreapi
