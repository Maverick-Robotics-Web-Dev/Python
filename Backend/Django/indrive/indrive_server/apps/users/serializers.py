from django.db.models import Model

from apps.users.models import UserModel
from customs.serializers.model_custom_serializer import ModelCustomSerializer


class UserSerializer(ModelCustomSerializer):
    class Meta:
        model: UserModel = UserModel
        # fields: str | list = '__all__'
        exclude: tuple | list = ['role']
        extra_kwargs = {
            'password': {'write_only': True},
            'status': {'write_only': True},
            'status_description': {'write_only': True},
            'create_at': {'write_only': True},
            'update_at': {'write_only': True},
        }
