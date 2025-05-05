from django.urls import (
    URLPattern,
    URLResolver
)

from .swagger.swagger_urls import url_swagger


urlpatterns: list[URLResolver | URLPattern] = url_swagger
