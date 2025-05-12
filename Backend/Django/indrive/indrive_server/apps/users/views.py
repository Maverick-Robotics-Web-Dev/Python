from typing import Self
from collections import OrderedDict

from django.db.models import Model
from django.db.models.query import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN
)

from apps.roles.models import RoleModel
from apps.roles.serializers import RoleSerializer
from apps.users.models import UserModel
from apps.users.serializers import UserSerializer
from customs.views.custom_view import CustomViewSet


class UserViewSet(CustomViewSet):
    model: UserModel = UserModel
    permission_classes = [IsAuthenticated]
    serializers: OrderedDict = {
        'default': UserSerializer,
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'create': UserSerializer,
        'partial_update': UserSerializer,
        'destroy': UserSerializer
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

            response: Response = Response(data, HTTP_404_NOT_FOUND)

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

        mdl: Model = self.get_object(pk)
        serializer: ModelSerializer = self.get_serializer(mdl)
        roles = RoleModel._default_manager.filter(userhasrolesmodel__id_user=mdl)
        roles_serializer = RoleSerializer(roles, many=True)

        data: OrderedDict = {
            'ok': 'OK',
            'data': {**serializer.data, 'roles': roles_serializer.data}
        }

        response: Response = Response(data, HTTP_200_OK)

        return response

    # def create(self: Self, request: Request):

    #     req_data: OrderedDict = request.data
    #     serializer: ModelSerializer = self.get_serializer(data=req_data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         data: OrderedDict = {
    #             'ok': 'OK',
    #             'msg': 'Creado Exitosamente',
    #             'data': serializer.data
    #         }
    #         response: Response = Response(data=data, status=HTTP_201_CREATED)
    #         return response

    #     data: OrderedDict = {
    #         'error': 'ERROR',
    #         'msg': serializer.errors
    #     }
    #     response: Response = Response(data, HTTP_400_BAD_REQUEST)
    #     return response

    def partial_update(self: Self, request: Request, pk: str = None):

        req_data: OrderedDict = request.data

        if str(request.user.id) != pk:
            data: OrderedDict = {
                'error': 'ERROR',
                'msg': 'No tienes permiso para actualizar este usuario'
            }
            response: Response = Response(data, HTTP_403_FORBIDDEN)

            return response

        mdl: Model = self.get_object(pk)
        serializer: ModelSerializer = self.get_serializer(mdl, data=req_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            roles = RoleModel._default_manager.filter(userhasrolesmodel__id_user=mdl)
            roles_serializer = RoleSerializer(roles, many=True)
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Actualizado Exitosamente',
                'data': {**serializer.data, 'roles': roles_serializer.data}
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
        mdl: Model = self.get_object(pk)
        serializer: ModelSerializer = self.get_serializer(mdl, data=req_data, partial=True)

        if serializer.is_valid():
            serializer.save(flag=True)
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Eliminado Exitosamente',
            }
            response: Response = Response(data, HTTP_200_OK)

            return response

        data = {
            'error': 'ERROR',
            'msg': serializer.errors
        }
        response = Response(data, HTTP_400_BAD_REQUEST)

        return response
