from typing import Self
from collections import OrderedDict

from django.db.models import Model

from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthSerializer
from apps.users.models import UserModel
from apps.users.serializers import UserSerializer
from apps.roles.models import RoleModel
from apps.roles.serializers import RoleSerializer
from apps.users.models import UserHasRolesModel
from customs.views.custom_view import CustomViewSet
from tools.methods.encrypt_data import encrypt_data, check_encrypted_data
from tools.methods.get_error import get_error_message
from tools.methods.create_relations import create_many_to_many_relation


class AuthViewSet(CustomViewSet):

    model: UserModel = UserModel
    permission_classes = [AllowAny]
    serializers: OrderedDict = {
        'default': UserSerializer,
        'sign_in': AuthSerializer
    }

    def custom_token_for_user(self: Self, user: Model):
        refresh_token: RefreshToken = RefreshToken.for_user(user)
        refresh_token.payload.pop('user_id')
        refresh_token.payload.update({'id': user.id, 'name': user.name})

        return refresh_token

    @action(methods=['POST'], detail=False)
    def sign_up(self: Self, request: Request):
        req_data: OrderedDict = request.data

        if req_data.get('password'):
            hashed_password: str = encrypt_data(req_data.pop('password'))
            req_data.update({'password': hashed_password})

        serializer: ModelSerializer = self.get_serializer(data=req_data)

        if serializer.is_valid():
            user = serializer.save()
            client_role = create_many_to_many_relation(model_to_get=RoleModel, many_to_many_model=UserHasRolesModel, model_created=user, serializer_model_to_get=RoleSerializer, id_model_get='CLIENT',  column_name='id_user', col_name='id_role')
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Creado Exitosamente',
                'data': {**serializer.data,  'roles': client_role}
            }
            response: Response = Response(data=data, status=HTTP_201_CREATED)
            return response

        data: OrderedDict = {
            'error': 'ERROR',
            'msg': get_error_message(serializer.errors.items())
        }
        response: Response = Response(data, HTTP_400_BAD_REQUEST)
        return response

    @action(methods=['POST'], detail=False)
    def sign_in(self: Self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            data: OrderedDict = {
                'error': 'ERROR',
                'msg': 'El email y password son obligatorios'
            }
            response: Response = Response(data=data, status=HTTP_400_BAD_REQUEST)

            return response

        serializer: AuthSerializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            data: OrderedDict = {
                'error': 'ERROR',
                'msg': get_error_message(serializer.errors.items())
            }
            response: Response = Response(data=data, status=HTTP_400_BAD_REQUEST)

            return response

        try:
            user: UserModel = self.model._default_manager.get(email=email, status=True)

        except self.model.DoesNotExist:
            data = {
                'error': 'ERROR',
                'msg': 'Email Incorrecto'
            }
            response: Response = Response(data=data, status=HTTP_401_UNAUTHORIZED)

            return response

        if check_encrypted_data(password.encode(), user.password.encode()):
            jw_token: RefreshToken = self.custom_token_for_user(user)
            access_token: str = str(jw_token.access_token)
            roles = RoleModel._default_manager.filter(userhasrolesmodel__id_user=user)
            roles_serializer = RoleSerializer(roles, many=True)
            data: OrderedDict = {
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'lastname': user.lastname,
                    'email': user.email,
                    'phone': user.phone,
                    'image': request.build_absolute_uri(user.image.url),
                    'notification_token': user.notification_token,
                    'roles': roles_serializer.data
                },
                'auth': {
                    'token': 'Bearer ' + access_token
                }
            }
            response: Response = Response(data=data, status=HTTP_200_OK)

            return response

        else:
            data = {
                'error': 'ERROR',
                'msg': 'Contraseña Incorrecta'
            }
            response: Response = Response(data=data, status=HTTP_403_FORBIDDEN)

            return response
