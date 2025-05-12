from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import UserModel


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):

        try:
            user_id = validated_token.get('id')
        except KeyError:
            raise AuthenticationFailed('Token contained no recognizable user identification')
        try:
            user = UserModel._default_manager.get(id=user_id)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        user.is_authenticated = True

        return user
