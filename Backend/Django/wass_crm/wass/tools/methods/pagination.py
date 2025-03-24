from typing import Any
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin


class Custom_Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data) -> dict[str, Any]:
        return {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'results': data
        }
