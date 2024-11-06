from django.urls import URLPattern, path

from .swagger_view import schema_view

url_swagger: list[URLPattern] = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
