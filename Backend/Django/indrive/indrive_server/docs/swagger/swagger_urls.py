from django.urls import URLPattern, path

from .swagger_view import schema_view

url_swagger: list[URLPattern] = [
    path(route='', view=schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(route='swagger<format>/', view=schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(route='swagger/', view=schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
