from typing import Self
from collections import OrderedDict

from django.db.models import Model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout
)

from rest_framework.request import Request
from rest_framework.serializers import (
    Serializer,
    ValidationError
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.exceptions import TokenError

from core.settings import HOME_URL, CACV_KEY, INSTALLED_APPS


class AuthCustomSerializer(Serializer):

    mdl: Model = None

    def get_model(self: Self) -> Model:

        model: Model = self.mdl

        return model

    def login(self: Self, request: Request) -> None:

        username: str = self.validated_data.get('user_name')
        password: str = self.validated_data.get('password')
        instance: Model = self.get_model()._default_manager.filter(user_name=username).first()

        if not instance:
            self._errors = {
                'error': 'ERROR',
                'msg': 'No existe el Usuario con esas credenciales'
            }
            raise ValidationError(self.errors, HTTP_204_NO_CONTENT)

        status: bool = instance.status
        active: bool = instance.is_active

        if not status and not active:
            self._errors = {
                'error': 'ERROR',
                'msg': 'No existe el Usuario con esas credenciales'
            }
            raise ValidationError(self.errors, HTTP_204_NO_CONTENT)

        user: AbstractBaseUser = authenticate(username=username, password=password)

        if user is not None:

            if user.login and user.is_authenticated:
                self._errors = {
                    'ok': 'OK',
                    'msg': 'Ya has iniciado sesión',
                    'home': HOME_URL
                }

                raise ValidationError(self.errors, HTTP_200_OK)

            jw_token: Token = RefreshToken.for_user(user)
            refresh_token: str = str(jw_token)
            access_token: str = str(jw_token.access_token)

            if CACV_KEY['SESSION_LOGIN']:
                django_login(request, user)

            setattr(user, 'login', True)
            user.save()
            self._data = {
                'id': user.id,
                'user_name': user.user_name,
                'login': user.login,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        else:
            self._errors = {
                'error': 'ERROR',
                'msg': 'Usuario o Contraseña Incorrectos'
            }

            raise ValidationError(self.errors, HTTP_400_BAD_REQUEST)

    def logout(self: Self, request: Request):

        validated_data: OrderedDict = self.validated_data

        try:
            user = request.user
            if CACV_KEY['SESSION_LOGIN']:
                django_logout(request)
                setattr(user, 'login', False)
                user.save()
            self._data = {
                'msg': 'Cerró sesión exitosamente'
            }

        except NotImplementedError:
            self._errors = {
                'error': 'ERROR',
                'msg': 'El Header no contiene el Access Token'
            }
            raise ValidationError(self.errors, HTTP_401_UNAUTHORIZED)

        if CACV_KEY['USE_JWT']:

            cookie_name = CACV_KEY['JWT_AUTH_COOKIE']

            if 'rest_framework_simplejwt.token_blacklist' in INSTALLED_APPS:

                # add refresh token to blacklist
                try:

                    black_token: str = validated_data.get('refresh_token')
                    token: RefreshToken = RefreshToken(black_token)
                    token.blacklist()

                except (TokenError, AttributeError, TypeError) as error:

                    if hasattr(error, 'args'):

                        if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:

                            self._errors = {
                                'error': 'ERROR',
                                'msg': error.args[0]
                            }
                            raise ValidationError(self.errors, HTTP_401_UNAUTHORIZED)

                        else:

                            self._errors = {
                                'error': 'ERROR',
                                'msg': 'Se ha producido un error.',
                                'errors': error
                            }
                            raise ValidationError(self.errors, HTTP_500_INTERNAL_SERVER_ERROR)

                    else:

                        self._errors = {
                            'error': 'ERROR',
                            'msg': 'Se ha producido un error.',
                            'errors': error
                        }
                        raise ValidationError(self.errors, HTTP_500_INTERNAL_SERVER_ERROR)

            elif not cookie_name:

                message = (
                    'Ni las cookies ni la lista negra están habilitadas, por lo que el token '
                    'no se ha eliminado del lado del servidor. Asegúrese de que el token se elimine del lado del cliente.',
                )

                self._errors = {
                    'error': 'ERROR',
                    'msg': message
                }
                raise ValidationError(self.errors, HTTP_200_OK)


class ChangePasswordCustomSerializer(Serializer):

    def validate(self: Self, data: OrderedDict) -> OrderedDict:

        if data['password'] != data['confirm_password']:

            raise ValidationError(
                {'password': 'No coinciden las contraseñas'})

        return data

    def change_password(self: Self, user: Model):

        try:
            validated_data: OrderedDict = self.validated_data
            password: str = validated_data.get('password')
            encrypted_password: str = make_password(password)
            setattr(user, 'password', encrypted_password)
            user.save()
            self._data = {
                'msg': 'Cambio de contraseña exitoso'
            }

        except Exception as error:
            self._errors = {
                'error': 'ERROR',
                'msg': 'Existen errores en la informaacion enviada',
                'errors': error
            }
            raise ValidationError(self.errors, HTTP_400_BAD_REQUEST)
