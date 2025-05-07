from typing import Self
from collections import OrderedDict

from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserModel
from apps.users.serializer import UserSerializer
from customs.views.custom_view import CustomViewSet
from tools.methods.encrypt_data import (encrypt_data, check_encrypted_data)


class AuthViewSet(CustomViewSet):

    model: UserModel = UserModel
    serializers: OrderedDict = {
        'default': UserSerializer,
    }

    @action(methods=['POST'], detail=False)
    def sign_up(self: Self, request: Request):
        req_data: OrderedDict = request.data
        encode_password = req_data.pop('password')
        hashed_password: str = encrypt_data(encode_password)
        req_data.update({'password': hashed_password})

        serializer: ModelSerializer = self.get_serializer(data=req_data)

        if serializer.is_valid():
            serializer.save()
            data: OrderedDict = {
                'ok': 'OK',
                'msg': 'Creado Exitosamente',
                'data': serializer.data
            }
            response: Response = Response(data=data, status=HTTP_201_CREATED)
            return response

        data: OrderedDict = {
            'error': 'ERROR',
            'msg': serializer.errors
        }
        response: Response = Response(data, HTTP_400_BAD_REQUEST)
        return response

    @action(methods=['POST'], detail=False)
    def sign_in(self: Self, request: Request):
        email: str = request.data.get('email')
        password: str = request.data.get('password')

        if not email or not password:
            data: OrderedDict = {
                'error': 'ERROR',
                'msg': 'El email y password son obligatorios'
            }
            response: Response = Response(data=data, status=HTTP_400_BAD_REQUEST)

            return response

        try:
            user: UserModel = self.model.objects.get(email=email, status=True)

        except self.model.DoesNotExist:
            data = {
                'error': 'ERROR',
                'msg': 'Email Incorrecto'
            }
            response: Response = Response(data=data, status=HTTP_401_UNAUTHORIZED)

            return response

        if check_encrypted_data(password.encode('utf-8'), user.password.encode('utf-8')):
            jw_token: RefreshToken = RefreshToken.for_user(user=user)
            access_token: str = str(jw_token.access_token)
            data: OrderedDict = {
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'lastname': user.lastname,
                    'email': user.email,
                    'phone': user.phone,
                    'image': user.image,
                    'notification_token': user.notification_token
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
            response: Response = Response(data=data, status=HTTP_401_UNAUTHORIZED)

            return response
