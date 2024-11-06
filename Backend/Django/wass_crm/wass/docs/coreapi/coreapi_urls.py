from django.urls import URLResolver, path

from rest_framework.documentation import include_docs_urls

url_coreapi: list[URLResolver] = [
    path('coreapi/', include_docs_urls(title='WASS API'), name='schema-coreapi')
]
