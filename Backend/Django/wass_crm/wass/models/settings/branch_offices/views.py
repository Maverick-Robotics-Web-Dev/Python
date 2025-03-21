from typing import Self
from collections import OrderedDict

from django.db.models import Model
from django.db.models.query import QuerySet

from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT
)

from models.settings.branch_offices.models import BranchOfficesModel
from models.settings.branch_offices.serializers import BranchOfficesSerializer
from tools.views.multi_serializer import OwnCustomViewSet


class BranchOfficesViewSet(OwnCustomViewSet):

    model: Model = BranchOfficesModel
    serializers: OrderedDict = {
        'default': BranchOfficesSerializer,
        'list': BranchOfficesSerializer,
        'retrieve': BranchOfficesSerializer,
        'create': BranchOfficesSerializer,
        'partial_update': BranchOfficesSerializer,
        'destroy': BranchOfficesSerializer
    }

    def get_object(self: Self, pk: str) -> Model:

        try:

            mdl: Model = self.model
            obj: Model = mdl.objects.get(pk=pk, status=True)
            return obj

        except mdl.DoesNotExist:

            data: OrderedDict = {
                'error': 'ERROR',
                'msg': 'No existen coincidencias'
            }

            response: ValidationError = ValidationError(data, HTTP_204_NO_CONTENT)

            raise response

    def get_queryset(self: Self) -> QuerySet:

        query_res = self.queryset

        if query_res is None:
            mdl: Model = self.model
            response: Model = mdl.objects.filter(status=True).order_by('name')

            return response

        return query_res

    def list(self: Self, request: Request) -> Response:

        query_res: QuerySet = self.get_queryset()

        if not query_res:
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'No existen datos',
            }
            response: Response = Response(data, HTTP_200_OK)

            return response

        serializer: ModelSerializer = self.get_serializer(query_res, many=True)

        data: OrderedDict = {
            'ok': 'OK',
            'data': serializer.data,
        }

        response: Response = Response(data, HTTP_200_OK)

        return response

    def retrieve(self: Self, request: Request, pk: str = None):

        obj: Model = self.get_object(pk)
        serializer: ModelSerializer = self.get_serializer(obj)

        data: OrderedDict = {
            'ok': 'OK',
            'data': serializer.data
        }

        response: Response = Response(data, HTTP_200_OK)

        return response

    def create(self: Self, request: Request):

        req_data: OrderedDict = request.data

        if 'name' in req_data.keys():
            names = self.model.objects.values_list('name', flat=True)
            search: str = req_data.get('name')

            if search in names:
                data: OrderedDict = {
                    'error': 'ERROR',
                    'msg': 'El nombre de la sucursal ya existe'
                }
                response: Response = Response(data, HTTP_400_BAD_REQUEST)
                return response

        serializer: ModelSerializer = self.get_serializer(data=req_data)

        if serializer.is_valid():
            serializer.save()
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Creado Exitosamente',
                'data': serializer.data
            }
            response: Response = Response(data, HTTP_201_CREATED)
            return response

        data: OrderedDict = {
            'error': 'ERROR',
            'msg': serializer.errors
        }
        response: Response = Response(data, HTTP_400_BAD_REQUEST)
        return response

    def partial_update(self: Self, request: Request, pk: str = None):

        req_data: OrderedDict = request.data
        obj: Model = self.get_object(pk)

        if 'name' in req_data.keys():
            names = self.model.objects.values_list('name', flat=True)
            search: str = req_data.get('name')

            if (search in names) and (str(obj.id) != pk):
                data: OrderedDict = {
                    'error': 'ERROR',
                    'msg': 'El nombre de la sucursal ya existe'
                }
                response: Response = Response(data, HTTP_400_BAD_REQUEST)
                return response

        serializer: ModelSerializer = self.get_serializer(obj, data=req_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Actualizado Exitosamente',
                'data': serializer.data
            }
            response: Response = Response(data, HTTP_201_CREATED)

            return response

        data: OrderedDict = {
            'error': 'ERROR',
            'msg': serializer.errors
        }
        response: Response = Response(data, HTTP_400_BAD_REQUEST)

        return response

    def destroy(self: Self, request: Request, pk: str = None):

        req_data: OrderedDict = request.data
        obj: Model = self.get_object(pk)
        serializer: ModelSerializer = self.get_serializer(obj, data=req_data, partial=True)

        if serializer.is_valid():
            serializer.save(flag=True)
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Eliminado Exitosamente',
            }
            response: Response = Response(data, HTTP_200_OK)

            return response

        self.data = {
            'error': 'ERROR',
            'msg': serializer.errors
        }
        response = Response(data, HTTP_400_BAD_REQUEST)

        return response

    @action(methods=['get'], detail=False)
    def list_pagination(self: Self, request: Request) -> Response:

        query_res: QuerySet = self.get_queryset()

        if not query_res:
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'No existen datos',
            }
            response: Response = Response(data, HTTP_200_OK)

            return response

        query_page = self.paginate_queryset(query_res)

        if query_page is not None:
            serializer: ModelSerializer = self.get_serializer(query_page, many=True)
            pagination: OrderedDict = self.get_paginated_response(serializer.data)

            data: OrderedDict = {
                'ok': 'OK',
                'next': pagination['next'],
                'previous': pagination['previous'],
                'count': pagination['count'],
                'pages': pagination['pages'],
                'current': pagination['current'],
                'data': pagination['results'],
            }

            response: Response = Response(data, HTTP_200_OK)

            return response

        serializer: ModelSerializer = self.get_serializer(query_res, many=True)

        data: OrderedDict = {
            'ok': 'OK',
            'data': serializer.data,
        }

        response: Response = Response(data, HTTP_200_OK)

        return response
