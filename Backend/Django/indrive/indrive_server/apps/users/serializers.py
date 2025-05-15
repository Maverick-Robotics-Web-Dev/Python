from apps.users.models import UserModel
from customs.serializers.custom_model_serializer import CustomModelSerializer


class UserSerializer(CustomModelSerializer):
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
