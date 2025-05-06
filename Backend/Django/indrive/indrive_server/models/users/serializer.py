from django.db.models import Model

from models.users.models import UserModel
from customs.serializers.model_custom_serializer import ModelCustomSerializer


class UserSerializer(ModelCustomSerializer):
    class Meta:
        model: Model = UserModel
        fields: str | list = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'status': {'write_only': True},
            'status_description': {'write_only': True},
            'create_at': {'write_only': True},
            'update_at': {'write_only': True}
        }
