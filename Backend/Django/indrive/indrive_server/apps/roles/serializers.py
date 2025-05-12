from apps.roles.models import RoleModel
from customs.serializers.custom_model_serializer import CustomModelSerializer


class RoleSerializer(CustomModelSerializer):
    class Meta:
        model: RoleModel = RoleModel
        fields: str | list = '__all__'
        extra_kwargs = {
            'status': {'write_only': True},
            'status_description': {'write_only': True},
            'create_at': {'write_only': True},
            'update_at': {'write_only': True}
        }
